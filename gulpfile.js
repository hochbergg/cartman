// -- Dependencies --
var browserify = require("browserify");
var buffer     = require("vinyl-buffer");
var gulp       = require("gulp");
var concat     = require("gulp-concat");
var gutil      = require("gulp-util");
var less       = require("gulp-less");
var minifycss  = require("gulp-minify-css");
var sourcemaps = require("gulp-sourcemaps");
var source     = require("vinyl-source-stream");
var watchify   = require("watchify");
var watchless  = require("gulp-watch-less");

/* -- Tasks Commands -- */
// Run `gulp b` to build the files and exit.
gulp.task("build", buildAll);
gulp.task("b", buildAll);
// Run `gulp w` to build the file and activate watchify (blocking forever).
gulp.task("watch", watchAll);
gulp.task("w", watchAll);
gulp.task("default", watchAll);

// Main production task.
gulp.task("production", production);

gulp.task("event_api", function() {
  return gulp.src(["./public/user_app/services/event_api.js",
                   "./public/user_app/comm.js",
                   "./public/bower_components/jquery/dist/jquery.min.js"])
    .pipe(concat("event_api_all.js"))
    .pipe(gulp.dest('./public/user_app/dist/'));
});

/* -- Paths -- */
var paths = {
  auth_app_path: "./public/auth_app",
  user_app_path: "./public/user_app",

  main_app_file: "app/app.js",
  main_less_file: "styles/all.less",
  dest_path: "dist",
  dest_file: "bundle.js",
  map_file: "bundle.js.map",
};
var bundled_app_paths = [
  paths.auth_app_path,
  paths.user_app_path,
];

/* -- Tasks -- */
function bundleAppFilesAll() {
  bundlers.forEach(function(bundler_params) {
      bundleAppFiles(bundler_params.bundler, bundler_params.app_path);
    });
}

function watchAppFilesAll() {
  bundlers.forEach(function(bundler_params) {
      bundleAppFiles(bundler_params.watcher, bundler_params.app_path);
    });
}

function compileLessFilesAll() {
  bundlers.forEach(function(bundler_params) {
      compileLessFiles(bundler_params.app_path);
    });
}

function watchLessFilesAll() {
  bundlers.forEach(function(bundler_params) {
      compileLessFiles(bundler_params.app_path);
      watchLessFiles(bundler_params.app_path);
    });
}

function buildAll() {
  bundleAppFilesAll();
  compileLessFilesAll();
  bundleEventAPI();
}

function watchAll() {
  watchAppFilesAll();
  watchLessFilesAll();
  watchEventAPI();
}

function production() {
  buildAll();
}

function bundleEventAPI() {
  var app_path = "./public/user_app/app/services";
  var app_file = app_path + "/" + "event_api.js";

  // Build the simple browserify bundler.
  var bundler = browserify(app_file, watchify.args);
  bundler.transform("brfs");

  bundleEventAPIFiles(bundler);

}

function watchEventAPI() {
  var app_path = "./public/user_app/app/services";
  var app_file = app_path + "/" + "event_api.js";

  // Build the watchify bundler that updates continuously.
  var watcher = watchify(browserify(app_file, watchify.args));
  watcher.transform("brfs");
  watcher.on("update", function() {
    bundleEventAPIFiles(watcher);
  });

  bundleEventAPIFiles(watcher);

}

function bundleEventAPIFiles(bundler) {
  var dest_path = "./public/user_app/";
  var dest_file = "dist" + "/" + "event_api_bundle.js";

  gutil.log("Bundling files for app: event_api");

  return bundler.bundle()
    // Log errors if they happen.
    .on("error", gutil.log.bind(gutil, "Browserify Error:"))
    .pipe(source(dest_file))
    // Add sourcemaps.
      .pipe(buffer())
      .pipe(sourcemaps.init({ loadMaps: true }))
      .pipe(sourcemaps.write("./"))
    // Write to destination folder.
    .pipe(gulp.dest(dest_path));

}

/* -- Functions -- */
function bundleAppFiles(bundler, app_path) {
  var dest_file = paths.dest_path + "/" + paths.dest_file;
  gutil.log("Bundling files for app: " + app_path);

  return bundler.bundle()
    // Log errors if they happen.
    .on("error", gutil.log.bind(gutil, "Browserify Error:"))
    .pipe(source(dest_file))
    // Add sourcemaps.
      .pipe(buffer())
      .pipe(sourcemaps.init({ loadMaps: true }))
      .pipe(sourcemaps.write("./"))
    // Write to destination folder.
    .pipe(gulp.dest(app_path));
}

function compileLessFiles(app_path) {
  var less_file = app_path + "/" + paths.main_less_file;
  var dest_path = app_path + "/" + paths.dest_path;
  gutil.log("Compiling LESS files for app: " + app_path);

  return gulp
    .src(less_file)
    .pipe(less())
    .pipe(minifycss({inliner: { timeout: 10000 }}))
    .pipe(gulp.dest(dest_path));
}

function watchLessFiles(app_path) {
  var less_file = app_path + "/" + paths.main_less_file;
  var dest_path = app_path + "/" + paths.dest_path;
  gutil.log("Watching LESS files for app: " + app_path);

  return watchless(less_file)
    .pipe(less().on("error", function(err){
        gutil.log(err);
        this.emit('end');
      }))
    .pipe(gulp.dest(dest_path));
}

/* -- Setup -- */
// Set up the bundler with Watchify and Browserify for each app.
bundlers = bundled_app_paths.map(function(app_path) {
  var app_file = app_path + "/" + paths.main_app_file;
  var less_file = app_path + "/" + paths.main_less_file;
  
  // Build the simple browserify bundler.
  var bundler = browserify(app_file, watchify.args);
  bundler.transform("brfs");

  // Build the watchify bundler that updates continuously.
  var watcher = watchify(browserify(app_file, watchify.args));
  watcher.transform("brfs");
  watcher.on("update", function() {
      bundleAppFiles(watcher, app_path);
    });

  return {
      app_path: app_path,
      bundler: bundler,
      watcher: watcher,
    };
});
