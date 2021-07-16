# Gradle 使用

## Gradle 是什么？

Gradle是一个自动化构建工具。

它使用DSL作为配置语法，而不是xml。默认是groovy语言，同样支持同是jvm语言的scala、java、kotlin等语言。

## Gradle 为什么难以掌握

因为知其然，而不知其所以然。

已build.gradle为例，大量的闭包的使用和语法糖，让文件看起来像是配置文件，但其实是正经的代码。

## 代码脱糖

1. apply是Project的一个方法，参数是一个map，plugin是key，'java'是value

```groovy
apply plugin: 'java'
// equals
apply(plugin: 'java')

apply from: 'segway.gradle'
// equals
apply([from: 'segway.gradle'])
```

2. buildscript 是Project的一个方法，参数是一个闭包。提供一个ScriptHandler对象。

```groovy
buildscript {
    // 
}
// equals
buildscript {ScriptHandler h ->
    // 
}
// equals
buildscript ({ScriptHandler h ->
    // 
})
```

3. dependencies 也是Project的一个方法，参数是一个闭包，提供一个DependencyHandler对象

```groovy
dependencies {
    classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:${kotlin_version}"
}
// equals
dependencies { DependencyHandler i ->
    add("classpath", "org.jetbrains.kotlin:kotlin-gradle-plugin:${kotlin_version}")
}
// equals
dependencies { 
    it.add("classpath", "org.jetbrains.kotlin:kotlin-gradle-plugin:${kotlin_version}")
}
// equals
dependencies { DependencyHandler i ->
    i.add("classpath", "org.jetbrains.kotlin:kotlin-gradle-plugin:${kotlin_version}")
}
// equals
dependencies ({ DependencyHandler i ->
    i.add("classpath", "org.jetbrains.kotlin:kotlin-gradle-plugin:${kotlin_version}")
})
```

4. allprojects也是Project的一个方法，参数是一个闭包、重载函数还可以接收一个Action<Project>对象。

```groovy
allprojects {
}
// equals
allprojects { Project p ->
}
// equals
allprojects ({ Project p ->
})
// equals，实测语法通过，构建失败了。
allprojects (new Action<Project>() {
    @Override
    void execute(Project project) {
        
    }
}
```

5. 同样的，setting.gradle 里的include，也是一个方法，接收一个路径数组。

```groovy
// class Settings
void include(String... projectPaths);
```

6. resolve

```groovy
configurations.all {
    resolutionStrategy.force bugsnag_android
}
// equals
configurations.all { Configuration c ->
    c.resolutionStrategy.force bugsnag_android
}
// equals
configurations.all(new Action<Configuration>() {
    @Override
    void execute(Configuration files) {
        files.getResolutionStrategy().force(bugsnag_android)
    }
})
```

7. compile/implementation/api 等

```groovy
alphaImplementation leakcanary_debug
// equals
add('alphaImplementation', 'leakcanary_debug')

DefaultComponentDependencies.java
// 最终执行
@Override
public void implementation(Object notation, Action<? super ExternalModuleDependency> action) {
    ExternalModuleDependency dependency = (ExternalModuleDependency) getDependencyHandler().create(notation);
    action.execute(dependency);
    implementation.getDependencies().add(dependency);
}

// DefaultDependencyHandler.java
private Dependency doAddRegularDependency(Configuration configuration, Object dependencyNotation, Closure<?> configureClosure) {
    Dependency dependency = create(dependencyNotation, configureClosure);
    configuration.getDependencies().add(dependency);
    return dependency;
}

private Dependency doAddProvider(Configuration configuration, Provider<?> dependencyNotation, Closure<?> configureClosure) {
    Provider<Dependency> lazyDependency = dependencyNotation.map(lazyNotation -> create(lazyNotation, configureClosure));
    configuration.getDependencies().addLater(lazyDependency);
    // Return null here because we don't want to prematurely realize the dependency
    return null;
}

private Dependency doAddConfiguration(Configuration configuration, Configuration dependencyNotation) {
    Configuration other = dependencyNotation;
    if (!configurationContainer.contains(other)) {
        throw new UnsupportedOperationException("Currently you can only declare dependencies on configurations from the same project.");
    }
    configuration.extendsFrom(other);
    return null;
}
```

8. task clean

```groovy
语法变形
TaskDefinitionScriptTransformer
task clean(type: Delete) {
// equals
task(type: Delete, name: "clean") {
```

## Project

Project接口，gradle的核心概念，代表当前项目。

## Setting

Settings接口，代表设置当前项目设置

## Task

构建的基本执行单元，根据依赖，形成一张图。

## 闭包

代码块，可以理解为一个lambda函数。

groovy
kotlin/kts
plugin

buildscript { ScriptHandler h ->
    println '#############'
    println h.toString()
    println h.class.name
    println this.class.name
    println this.class.location
    println h.sourceURI
    println h.sourceFile
    println '#############'

output:
#############
org.gradle.api.internal.initialization.DefaultScriptHandler@62479c75
org.gradle.api.internal.initialization.DefaultScriptHandler
build_4tfwdlp8rg93wd7cltq3bke2u
file:/Users/leochou/.gradle/caches/jars-8/b864f263c0b664bd0734815542ffe821/cp_proj.jar
file:/Users/leochou/Work/app-apr-food-deliver/build.gradle
/Users/leochou/Work/app-apr-food-deliver/build.gradle
#############

## 后续任务

[ ] 文档整理

## 引用

[gradle DSL](https://docs.gradle.org/current/dsl/index.html)

[android DSL](https://developer.android.com/reference/tools/gradle-api)

[android DSL 早期版本](https://google.github.io/android-gradle-dsl/)

[android DSL 早期版本 Github](https://github.com/google/android-gradle-dsl)

[Task 另类语法](https://zhuanlan.zhihu.com/p/365577252)