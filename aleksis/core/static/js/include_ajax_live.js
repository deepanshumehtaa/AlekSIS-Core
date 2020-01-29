const asyncIntervals = [];

const runAsyncInterval = async (cb, interval, intervalIndex) => {
  await cb();
  if (asyncIntervals[intervalIndex]) {
    setTimeout(() => runAsyncInterval(cb, interval, intervalIndex), interval);
  }
};

const setAsyncInterval = (cb, interval) => {
  if (cb && typeof cb === "function") {
    const intervalIndex = asyncIntervals.length;
    asyncIntervals.push(true);
    runAsyncInterval(cb, interval, intervalIndex);
    return intervalIndex;
  } else {
    throw new Error('Callback must be a function');
  }
};

const clearAsyncInterval = (intervalIndex) => {
  if (asyncIntervals[intervalIndex]) {
    asyncIntervals[intervalIndex] = false;
  }
};

let dashboard_interval = setAsyncInterval(async () => {
  console.log('fetching new data');
  const promise = new Promise((resolve) => {
    $('#dashboard').load("/?include_by_ajax_full_render=1 #dashboard");
    resolve(1);
  });
  await promise;
  console.log('data fetched successfully');
}, 15000);

$(document).on('include_by_ajax_all_loaded', function() {
    console.log('Now all placeholders are loaded and replaced with content');
})
