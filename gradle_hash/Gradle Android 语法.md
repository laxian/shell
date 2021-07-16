# Gradle 使用

> 本文分析基于gradle-6.5，鉴于gradle版本更新较快，不同版本间可能语法或代码实例或许会有差异

## Task



## Extension

### 是什么

带属性的类，没有任何接口和类型。注册到project.extensions，即可扩展。

以官方内置publishing扩展为例：

```java
public interface PublishingExtension {

    String NAME = "publishing";

    RepositoryHandler getRepositories();

    void repositories(Action<? super RepositoryHandler> configure);

    PublicationContainer getPublications();

    void publications(Action<? super PublicationContainer> configure);
}
```

对应使用格式：

```groovy
publishing {
  repositories {
    // Create an ivy publication destination named “releases”
    ivy {
      name "releases"
      url "http://my.org/ivy-repos/releases"
    }
  }
  publications {
    myPublicationName(MavenPublication) {
      // Configure the publication here
    }
  }
}
```

### 怎么做

看一个注释里的例子

```groovy
 * // Extensions are just plain objects, there is no interface/type
 * class MyExtension {
 *   String foo
 *
 *   MyExtension(String foo) {
 *     this.foo = foo
 *   }
 * }
 *
 * // Add new extensions via the extension container
 * project.extensions.create('custom', MyExtension, "bar")
 * //                       («name»,   «type»,       «constructor args», …)
 *
 * // extensions appear as properties on the target object by the given name
 * assert project.custom instanceof MyExtension
 * assert project.custom.foo == "bar"
 *
 * // also via a namespace method
 * project.custom {
 *   assert foo == "bar"
 *   foo = "other"
 * }
 * assert project.custom.foo == "other"
```

最后，关于扩展，我们使用最多的就是扩展属性了，通过

```groovy
ext {
    junit = "junit:junit:4.12"
}
```

是的，这也是个扩展功能，实现类是`ExtraPropertiesExtension`，感兴趣的可以自行查看源代码。

### Android相关

build.gradle顶级配置块，有些是内置方法，如：`dependencies`、`buildscript`，`allprojects`。特定平台，特定功能的配置块，多是通过扩展实现的。

Android代码块也是，下面是一个android项目的示例：

```groovy
android {
    compileSdkVersion SPCompileSdkVersion
    buildToolsVersion SPBuildToolsVersion

    defaultConfig {
        applicationId "com.segway.xxx"
        minSdkVersion SPMinSdkVersion
        targetSdkVersion SPTargetSdkVersion
        versionCode Integer.MAX_VALUE
        versionName SPVersionName
        resConfigs "zh"
        multiDexEnabled true

        ndk {
            abiFilters "arm64-v8a"
        }
        manifestPlaceholders = [GRADLE_SHARED_USER_ID: 'android.uid.system']

        renderscriptTargetApi 24
        renderscriptSupportModeEnabled true
        vectorDrawables.useSupportLibrary = true
    }

    signingConfigs {
        release {
            keyAlias 'platform'
            keyPassword 'android'
            storeFile file('/Users/leochou/Downloads/platform.keystore')//签名文件路径
            storePassword 'android'
            v2SigningEnabled true
        }
        debug {
            keyAlias 'platform'
            keyPassword 'android'
            storeFile file('/Users/leochou/Downloads/platform.keystore')//签名文件路径
            storePassword 'android'
            v2SigningEnabled true
        }
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
        alpha {
            initWith debug
            manifestPlaceholders = [GRADLE_SHARED_USER_ID: '']
            ndk {
                abiFilters "arm64-v8a", "x86"
            }
        }
        debug {
            signingConfig signingConfigs.release
        }
    }

    compileOptions {
        targetCompatibility 1.8
        sourceCompatibility 1.8
    }

    viewBinding {
        enabled = true
    }

    lintOptions {
        abortOnError false
    }

    buildTypes.all { type ->
        type.matchingFallbacks = ['debug']
    }

    android.applicationVariants.all { variant ->
        variant.outputs.all {
            outputFileName = "segway-delivery-${variant.name}-${SPVersionName}-${SPGitHash}.apk"
        }
    }
}
```

