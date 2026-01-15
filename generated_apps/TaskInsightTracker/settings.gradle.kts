pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "TitanFinance"

// Core modules
include(":app")
include(":core:common")
include(":core:network")
include(":core:database")
include(":core:ui")
include(":core:testing")

// Feature modules
include(":feature:tasks")
include(":feature:analytics")
