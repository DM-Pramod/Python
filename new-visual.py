C:\Users\PramodDM\PROJECTS\ProjectBike\travel_app>flutter run  
Launching lib\main.dart on sdk gphone64 x86 64 in debug mode...
warning: [options] source value 8 is obsolete and will be removed in a future release
warning: [options] target value 8 is obsolete and will be removed in a future release
warning: [options] To suppress warnings about obsolete options, use -Xlint:-options.
3 warnings
warning: [options] source value 8 is obsolete and will be removed in a future release
warning: [options] target value 8 is obsolete and will be removed in a future release
warning: [options] To suppress warnings about obsolete options, use -Xlint:-options.
3 warnings
warning: [options] source value 8 is obsolete and will be removed in a future release
warning: [options] target value 8 is obsolete and will be removed in a future release
warning: [options] To suppress warnings about obsolete options, use -Xlint:-options.
Note: Some input files use or override a deprecated API.
Note: Recompile with -Xlint:deprecation for details.
3 warnings

FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':flutter_plugin_android_lifecycle:compileDebugJavaWithJavac'.
> Could not resolve all files for configuration ':flutter_plugin_android_lifecycle:androidJdkImage'.
   > Failed to transform core-for-system-modules.jar to match attributes {artifactType=_internal_android_jdk_image, org.gradle.libraryelements=jar, org.gradle.usage=java-runtime}.
      > Execution failed for JdkImageTransform: C:\Users\PramodDM\AppData\Local\Android\sdk\platforms\android-34\core-for-system-modules.jar.        
         > Error while executing process C:\Users\PramodDM\Android\jbr\bin\jlink.exe with arguments {--module-path C:\Users\PramodDM\.gradle\caches\transforms-3\c7f5d563e1877cd5931fe99b4d6b075f\transformed\output\temp\jmod --add-modules java.base --output C:\Users\PramodDM\.gradle\caches\transforms-3\c7f5d563e1877cd5931fe99b4d6b075f\transformed\output\jdkImage --disable-plugin system-modules}

* Try:
> Run with --stacktrace option to get the stack trace.
> Run with --info or --debug option to get more log output.
> Run with --scan to get full insights.
> Get more help at https://help.gradle.org.

BUILD FAILED in 13s
Running Gradle task 'assembleDebug'...                             14.6s

┌─ Flutter Fix ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [!] This is likely due to a known bug in Android Gradle Plugin (AGP) versions less than 8.2.1, when                                   │
│   1. setting a value for SourceCompatibility and                                                                                      │
│   2. using Java 21 or above.                                                                                                          │
│ To fix this error, please upgrade your AGP version to at least 8.2.1. The version of AGP that your project uses is likely defined in: │
│ C:\Users\PramodDM\PROJECTS\ProjectBike\travel_app\android\settings.gradle,                                                            │
│ in the 'plugins' closure (by the number following "com.android.application").                                                         │
│  Alternatively, if your project was created with an older version of the templates, it is likely                                      │
│ in the buildscript.dependencies closure of the top-level build.gradle:                                                                │
│ C:\Users\PramodDM\PROJECTS\ProjectBike\travel_app\android\build.gradle,                                                               │
│ as the number following "com.android.tools.build:gradle:".                                                                            │
│                                                                                                                                       │
│ For more information, see:                                                                                                            │
│ https://issuetracker.google.com/issues/294137077                                                                                      │
│ https://github.com/flutter/flutter/issues/156304                                                                                      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
Error: Gradle task assembleDebug failed with exit code 1

C:\Users\PramodDM\PROJECTS\ProjectBike\travel_app>flutter clean
Deleting build...                                                  168ms
Deleting .dart_tool...                                              16ms
Deleting Generated.xcconfig...                                       0ms
Deleting flutter_export_environment.sh...                            0ms
Deleting ephemeral...                                                1ms
Deleting ephemeral...                                                0ms
Deleting .flutter-plugins-dependencies...                            0ms
Deleting .flutter-plugins...                                         1ms

PLEASE TELL ME IF IM MISSING ANYTHING FROM THESE 2 GRADLE FILES
1) ANDROID/BUILD.GRADLE

buildscript{
    ext.kotlin_version = '2.0.20'
    repositories{
        google()
        mavenCentral()
    }
    dependencies {
        classpath "com.android.tools.build:gradle:8.2.1"
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
        classpath "com.google.gms:google-services:4.4.2"
      
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.buildDir = "../build"
subprojects {
    project.buildDir = "${rootProject.buildDir}/${project.name}"
}
subprojects {
    project.evaluationDependsOn(":app")
}

tasks.register("clean", Delete) {
    delete rootProject.buildDir
}


2) ANDROID/APP/BUILD.GRADDLE
plugins {
    id "com.android.application"
    id "kotlin-android"
    id "com.google.gms.google-services"
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id "dev.flutter.flutter-gradle-plugin"
}

dependencies {
    // Import the Firebase BoM
    implementation platform('com.google.firebase:firebase-bom:33.8.0')

    // Add Firebase Analytics
    implementation 'com.google.firebase:firebase-analytics'

    // Add additional Firebase dependencies if needed
    // implementation 'com.google.firebase:firebase-auth'
}

android {
    namespace = "com.example.travel_app"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_1_8
    }

    defaultConfig {
        applicationId = "com.example.travel_app"
        minSdk = 23  // Ensure minSdkVersion is set to at least 23
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }
}

                                                                                                                      
