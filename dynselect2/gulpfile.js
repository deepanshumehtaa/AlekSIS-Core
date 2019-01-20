//Include required modules
// import * as gulp from "gulp";
// import * as babelify from "babelify";
// import * as browserify from "browserify";
// import * as source from "vinyl-source-stream";
var gulp = require("gulp"),
    babelify = require('babelify'),
    browserify = require("browserify"),
    connect = require("gulp-connect"),
    source = require("vinyl-source-stream")
// ;

//Default task. This will be run when no task is passed in arguments to gulp
// gulp.task("default", ["build", "startServer"]);

//Copy static files from html folder to build folder
// gulp.task("copyStaticFiles", function(){
//     return gulp.src("./src/html/*.*")
//         .pipe(gulp.dest("./build"));
// });

//Convert ES6 ode in all js files in src/js folder and copy to
//build folder as bundle.js
gulp.task("build", function () {
    return browserify({
        entries: ["./src/App.js"]
    })
        .transform(babelify.configure({
            presets: [
                "@babel/env",
                "@babel/react"
            ],
            plugins: ["@babel/plugin-proposal-class-properties"]

        }))
        .bundle()
        .pipe(source("bundle.js"))
        .pipe(gulp.dest("./build"))
        ;
});

//Start a test server with doc root at build folder and
//listening to 9001 port. Home page = http://localhost:9001
// gulp.task("startServer", function(){
//     connect.server({
//         root : "./build",
//         livereload : true,
//         port : 9001
//     });
// });