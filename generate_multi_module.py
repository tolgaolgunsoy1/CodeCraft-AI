#!/usr/bin/env python3
"""
Script to generate a multi-module Android app using the MultiModuleGenerator
"""

from backend.multi_module_generator import MultiModuleGenerator
import os
import json

def create_multi_module_app():
    """Generate Task & Insight Tracker multi-module app"""

    app_name = "TaskInsightTracker"
    features = ['tasks', 'analytics']

    # Generate the structure
    generator = MultiModuleGenerator()
    structure = generator.generate_module_structure(app_name, features)

    # Create base directory
    base_dir = f"generated_apps/{app_name}"
    if os.path.exists(base_dir):
        import shutil
        shutil.rmtree(base_dir)
    os.makedirs(base_dir, exist_ok=True)

    # Create root files
    for file_path, content in structure['root'].items():
        full_path = os.path.join(base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # Create app module
    app_dir = os.path.join(base_dir, 'app')
    os.makedirs(app_dir, exist_ok=True)
    for file_path, content in structure['app'].items():
        full_path = os.path.join(app_dir, file_path)
        if isinstance(content, str):
            # It's a placeholder for directory
            os.makedirs(full_path, exist_ok=True)
        else:
            # It's a file with content
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

    # Create core modules
    for module_name, module_files in structure['core'].items():
        module_dir = os.path.join(base_dir, 'core', module_name)
        os.makedirs(module_dir, exist_ok=True)
        for file_path, content in module_files.items():
            full_path = os.path.join(module_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

    # Create feature modules
    for feature_name, feature_files in structure['feature'].items():
        feature_dir = os.path.join(base_dir, 'feature', feature_name)
        os.makedirs(feature_dir, exist_ok=True)
        for file_path, content in feature_files.items():
            if isinstance(content, dict):
                # It's a subdirectory with files
                for sub_file, sub_content in content.items():
                    full_path = os.path.join(feature_dir, file_path, sub_file)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(sub_content)
            else:
                # It's a file
                full_path = os.path.join(feature_dir, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)

    # Create version catalog (libs.versions.toml)
    libs_versions = """[versions]
compose-compiler = "1.5.8"
compose-bom = "2024.05.00"
kotlin = "1.9.22"
hilt = "2.48"
retrofit = "2.9.0"
moshi = "1.15.0"
room = "2.6.1"
coil = "2.5.0"
junit = "4.13.2"
mockk = "1.13.9"
turbine = "1.0.0"

[libraries]
kotlin-stdlib = { module = "org.jetbrains.kotlin:kotlin-stdlib", version.ref = "kotlin" }
kotlinx-coroutines-android = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-android", version.ref = "kotlin" }

# Compose
compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }
compose-ui = { group = "androidx.compose.ui", name = "ui" }
compose-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
compose-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
compose-material3 = { group = "androidx.compose.material3", name = "material3" }
compose-material-icons-extended = { group = "androidx.compose.material", name = "material-icons-extended" }

# Hilt
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-compiler", version.ref = "hilt" }
hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version.ref = "hilt" }

# Network
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
retrofit-converter-moshi = { group = "com.squareup.retrofit2", name = "converter-moshi", version.ref = "retrofit" }
moshi = { group = "com.squareup.moshi", name = "moshi", version.ref = "moshi" }
moshi-codegen = { group = "com.squareup.moshi", name = "moshi-kotlin-codegen", version.ref = "moshi" }

# Database
room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }

# Image Loading
coil-compose = { group = "io.coil-kt", name = "coil-compose", version.ref = "coil" }

# Testing
junit = { group = "junit", name = "junit", version.ref = "junit" }
mockk = { group = "io.mockk", name = "mockk", version.ref = "mockk" }
turbine = { group = "app.cash.turbine", name = "turbine", version.ref = "turbine" }

[plugins]
android-application = { id = "com.android.application", version = "8.2.2" }
android-library = { id = "com.android.library", version = "8.2.2" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version = "1.9.22-1.0.16" }
hilt = { id = "com.google.dagger.hilt.android.plugin", version.ref = "hilt" }
"""

    libs_path = os.path.join(base_dir, 'gradle', 'libs.versions.toml')
    os.makedirs(os.path.dirname(libs_path), exist_ok=True)
    with open(libs_path, 'w', encoding='utf-8') as f:
        f.write(libs_versions)

    # Create gradle wrapper files (simplified)
    gradle_wrapper_dir = os.path.join(base_dir, 'gradle', 'wrapper')
    os.makedirs(gradle_wrapper_dir, exist_ok=True)

    gradle_wrapper_properties = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.5-bin.zip
networkTimeout=10000
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""

    with open(os.path.join(gradle_wrapper_dir, 'gradle-wrapper.properties'), 'w') as f:
        f.write(gradle_wrapper_properties)

    # Create gradlew scripts (simplified)
    gradlew_content = """#!/bin/bash
./gradlew "$@"
"""
    with open(os.path.join(base_dir, 'gradlew'), 'w') as f:
        f.write(gradlew_content)

    gradlew_bat_content = """@echo off
gradlew.bat %*
"""
    with open(os.path.join(base_dir, 'gradlew.bat'), 'w') as f:
        f.write(gradlew_bat_content)

    print(f"Multi-module app '{app_name}' generated successfully in {base_dir}")
    print(f"Features: {', '.join(features)}")
    print(f"Modules: app + core(common, network, database, ui, testing) + features({', '.join(features)})")

    return base_dir

if __name__ == "__main__":
    create_multi_module_app()