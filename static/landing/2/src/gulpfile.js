/**
 * Gulpfile
 * @author Am!n <Dornaweb.com>
*/
'use strict';

var gulp            = require('gulp'),
    sourcemaps      = require('gulp-sourcemaps'),
    stylus          = require('gulp-stylus'),
    rename          = require('gulp-rename'),
    notify          = require('gulp-notify'),
    nib             = require('nib'),
    svgSprite       = require('gulp-svg-sprites'),
    svgSprite2      = require('gulp-svg-sprite');

gulp.task('stylus', function(){
    return gulp.src(['./stylus/styles.styl'])
        .pipe(
            stylus({
                use: nib()
            })
        )
        .on( 'error', notify.onError(function (err){
            return err.message;
        }))
        .pipe( gulp.dest('../assets/css') );
});

gulp.task('compress', function(){
    return gulp.src(['./stylus/styles.styl'])
        .pipe(sourcemaps.init())
        .pipe(
            stylus({
                use: nib(),
                compress: true
            })
        )
        .on( 'error', notify.onError(function (err){
            return err.message;
        }))
        .pipe(rename({
            extname: '.min.css'
        }))
        .pipe(sourcemaps.write('.'))
        .pipe( gulp.dest('../assets/css') )
        // .pipe( notify({
        //     title: 'Stylus',
        //     message: 'CSS compiled!',
        //     icon: false,
        //     time: 1,
        // }));
});

gulp.task('svgsprite', function(){
    return gulp.src(['./svg/*.svg'])
        .pipe(
            svgSprite({
                baseSize: 16,
                mode: "symbols",
            })
        )
        .pipe( gulp.dest('./svg/pack') );
});

gulp.task('svgsprite2', function(){
    return gulp.src(['./svg/*.svg'])
    .pipe(svgSprite2({
        mode: {
            symbol: true,
            cleanupIDs: true
        },
        cleanupIDs: true
    }))
    .pipe(gulp.dest('./svg/pack2'));
});

gulp.task('default',function() {
    gulp.watch([
        './stylus/*.styl',
        './stylus/*.styl',
    ], function(event) {
        gulp.run( 'stylus', 'compress' );
    });
});
