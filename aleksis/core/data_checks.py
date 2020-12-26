import logging

from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Count
from django.utils.translation import gettext as _

import reversion
from templated_email import send_templated_mail

from .util.core_helpers import celery_optional, get_site_preferences


class SolveOption:
    name: str = "default"
    verbose_name: str = ""

    @classmethod
    def solve(cls, check_result: "DataCheckResult"):
        pass


class IgnoreSolveOption(SolveOption):
    name = "ignore"
    verbose_name = _("Ignore problem")

    @classmethod
    def solve(cls, check_result: "DataCheckResult"):
        check_result.solved = True
        check_result.save()


class DataCheck:
    name: str = ""
    verbose_name: str = ""
    problem_name: str = ""

    solve_options = {IgnoreSolveOption.name: IgnoreSolveOption}

    @classmethod
    def check_data(cls):
        pass

    @classmethod
    def solve(cls, check_result: "DataCheckResult", solve_option: str = "default"):
        with reversion.create_revision():
            cls.solve_options[solve_option].solve(check_result)

    @classmethod
    def register_result(cls, instance) -> "DataCheckResult":
        from aleksis.core.models import DataCheckResult

        ct = ContentType.objects.get_for_model(instance)
        result = DataCheckResult.objects.get_or_create(
            check=cls.name, content_type=ct, object_id=instance.id
        )
        return result


class DataCheckRegistry:
    def __init__(self):
        self.data_checks = []
        self.data_checks_by_name = {}
        self.data_checks_choices = []

    def register(self, check: DataCheck):
        self.data_checks.append(check)
        self.data_checks_by_name[check.name] = check
        self.data_checks_choices.append((check.name, check.verbose_name))
        return check


DATA_CHECK_REGISTRY = DataCheckRegistry()


@celery_optional
def check_data():
    for check in DATA_CHECK_REGISTRY.data_checks:
        logging.info(f"Run check: {check.verbose_name}")
        check.check_data()

    if get_site_preferences()["general__data_checks_send_emails"]:
        send_emails_for_data_checks()


def send_emails_for_data_checks():
    """Notify one or more recipients about new problems with data.

    Recipients can be set in dynamic preferences.
    """
    from .models import DataCheckResult  # noqa

    results = DataCheckResult.objects.filter(solved=False, sent=False)

    if results.exists():
        results_by_check = results.values("check").annotate(count=Count("check"))

        results_with_checks = []
        for result in results_by_check:
            results_with_checks.append(
                (DATA_CHECK_REGISTRY.data_checks_by_name[result["check"]], result["count"])
            )

        send_templated_mail(
            template_name="data_checks",
            from_email=get_site_preferences()["mail__address"],
            recipient_list=[
                p.email for p in get_site_preferences()["general__data_checks_recipients"]
            ],
            context={"results": results_with_checks},
        )

        logging.info("Sent notification email because of unsent data checks")

        results.update(sent=True)
