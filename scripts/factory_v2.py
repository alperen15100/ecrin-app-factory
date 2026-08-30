#!/usr/bin/env python3
import argparse, re
from pathlib import Path

a=argparse.ArgumentParser()
a.add_argument("--name",required=True); a.add_argument("--package",required=True)
x=a.parse_args(); name=x.name.strip(); pkg=x.package.strip()
if not re.fullmatch(r"[A-Za-z_]\w*(\.[A-Za-z_]\w*){2,}",pkg): raise SystemExit("Invalid package")
r=Path("generated-app"); pp=Path(*pkg.split("."))
def w(p,s):
 p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding="utf-8")

w(r/"settings.gradle.kts",'''pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }
rootProject.name="GeneratedApp"
include(":app")
''')
w(r/"build.gradle.kts",'''plugins {
 id("com.android.application") version "8.7.3" apply false
 id("org.jetbrains.kotlin.android") version "2.0.21" apply false
 id("org.jetbrains.kotlin.plugin.compose") version "2.0.21" apply false
}
''')
w(r/"gradle.properties",'''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
''')
w(r/"app/build.gradle.kts",f'''plugins {{
 id("com.android.application")
 id("org.jetbrains.kotlin.android")
 id("org.jetbrains.kotlin.plugin.compose")
}}
android {{
 namespace="{pkg}"
 compileSdk=35
 defaultConfig {{ applicationId="{pkg}"; minSdk=26; targetSdk=35; versionCode=1; versionName="1.0" }}
 buildFeatures {{ compose=true }}
 compileOptions {{ sourceCompatibility=JavaVersion.VERSION_17; targetCompatibility=JavaVersion.VERSION_17 }}
 kotlinOptions {{ jvmTarget="17" }}
}}
dependencies {{
 implementation(platform("androidx.compose:compose-bom:2024.12.01"))
 implementation("androidx.activity:activity-compose:1.10.0")
 implementation("androidx.compose.material3:material3")
 implementation("androidx.compose.ui:ui")
 implementation("androidx.compose.ui:ui-tooling-preview")
 debugImplementation("androidx.compose.ui:ui-tooling")
}}
''')
w(r/"app/src/main/res/values/styles.xml",'''<resources>
<style name="Theme.GeneratedApp" parent="android:style/Theme.Material.Light.NoActionBar">
<item name="android:statusBarColor">#0B0D0C</item>
<item name="android:navigationBarColor">#0B0D0C</item>
</style>
</resources>''')
w(r/"app/src/main/AndroidManifest.xml",f'''<manifest xmlns:android="http://schemas.android.com/apk/res/android">
<application android:label="{name}" android:theme="@style/Theme.GeneratedApp">
<activity android:name=".MainActivity" android:exported="true">
<intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter>
</activity>
</application>
</manifest>''')

kt = '''package __PKG__

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class MainActivity: ComponentActivity() {
 override fun onCreate(savedInstanceState: Bundle?) {
  super.onCreate(savedInstanceState)
  setContent { MaterialTheme { Home() } }
 }
}
@Composable fun Home() {
 var status by remember { mutableStateOf("Ready") }
 Surface(modifier=Modifier.fillMaxSize(),color=Color(0xFF0B0D0C)) {
  Column(modifier=Modifier.fillMaxSize().padding(24.dp),verticalArrangement=Arrangement.Center) {
   Text("__NAME__",color=Color.White,fontSize=34.sp,fontWeight=FontWeight.Bold)
   Spacer(Modifier.height(8.dp))
   Text("Built by Ecrin App Factory",color=Color(0xFF9CA3AF))
   Spacer(Modifier.height(30.dp))
   Card(modifier=Modifier.fillMaxWidth(),shape=RoundedCornerShape(24.dp),
    colors=CardDefaults.cardColors(containerColor=Color(0xFF151A17))) {
    Column(Modifier.padding(22.dp)) {
     Text("Factory generated Android project",color=Color.White,fontSize=18.sp,fontWeight=FontWeight.SemiBold)
     Spacer(Modifier.height(10.dp))
     Text("Kotlin • Jetpack Compose • GitHub Actions",color=Color(0xFF9CA3AF))
     Spacer(Modifier.height(22.dp))
     Button(onClick={status="Factory works ✓"},modifier=Modifier.fillMaxWidth(),
      colors=ButtonDefaults.buttonColors(containerColor=Color(0xFFB7FF3C),contentColor=Color.Black)) {
      Text("TEST APP",fontWeight=FontWeight.Bold)
     }
     Spacer(Modifier.height(16.dp))
     Text(status,color=Color(0xFFB7FF3C))
    }
   }
   Spacer(Modifier.height(24.dp))
   Text("Ecrin Labs",color=Color(0xFF6B7280))
  }
 }
}
'''.replace("__PKG__",pkg).replace("__NAME__",name.replace('"',''))
w(r/"app/src/main/java"/pp/"MainActivity.kt",kt)
print("Generated",name,pkg)
