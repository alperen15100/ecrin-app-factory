#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def safe_name(s):
    return s.replace('"', '').replace('\\', '').strip()[:50] or "Ecrin App"

def recipe_for(request):
    r = request.lower()
    has_image = any(x in r for x in ["image", "photo", "picture", "foto", "görsel", "resim"])
    has_pdf = "pdf" in r
    if has_image and has_pdf:
        return "image_to_pdf"
    raise SystemExit("V3 currently supports only the real Image-to-PDF recipe.")

ap = argparse.ArgumentParser()
ap.add_argument("--request", required=True)
ap.add_argument("--name", required=True)
ap.add_argument("--package", required=True)
args = ap.parse_args()

request = " ".join(args.request.split())
name = safe_name(args.name)
pkg = args.package.strip()

if not re.fullmatch(r"[A-Za-z_]\w*(\.[A-Za-z_]\w*){2,}", pkg):
    raise SystemExit("Invalid Android package name: " + pkg)

recipe = recipe_for(request)
root = Path("generated-app")
pp = Path(*pkg.split("."))

write(root / "settings.gradle.kts", '''pluginManagement {
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
rootProject.name = "GeneratedApp"
include(":app")
''')

write(root / "build.gradle.kts", '''plugins {
    id("com.android.application") version "8.7.3" apply false
    id("org.jetbrains.kotlin.android") version "2.0.21" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.0.21" apply false
}
''')

write(root / "gradle.properties", '''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
''')

write(root / "app/build.gradle.kts", f'''plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}}

android {{
    namespace = "{pkg}"
    compileSdk = 35

    defaultConfig {{
        applicationId = "{pkg}"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }}

    buildFeatures {{
        compose = true
    }}

    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}

    kotlinOptions {{
        jvmTarget = "17"
    }}
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

write(root / "app/src/main/res/values/styles.xml", '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.GeneratedApp" parent="android:style/Theme.Material.Light.NoActionBar">
        <item name="android:fontFamily">sans</item>
        <item name="android:windowLightStatusBar">false</item>
        <item name="android:statusBarColor">#0B0D0C</item>
        <item name="android:navigationBarColor">#0B0D0C</item>
    </style>
</resources>
''')

write(root / "app/src/main/AndroidManifest.xml", f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="true"
        android:label="{name}"
        android:supportsRtl="true"
        android:theme="@style/Theme.GeneratedApp">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
''')

main_kt = r'''package __PKG__

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Color as AndroidColor
import android.graphics.Paint
import android.graphics.pdf.PdfDocument
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.io.IOException
import kotlin.math.min

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { MaterialTheme { ImagePdfApp() } }
    }
}

@Composable
fun ImagePdfApp() {
    val context = androidx.compose.ui.platform.LocalContext.current
    var images by remember { mutableStateOf<List<Uri>>(emptyList()) }
    var status by remember { mutableStateOf("Select images to begin") }
    var isWorking by remember { mutableStateOf(false) }

    val picker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetMultipleContents()
    ) { uris ->
        images = uris
        status = if (uris.isEmpty()) "No images selected" else "${uris.size} image(s) selected"
    }

    val savePdf = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.CreateDocument("application/pdf")
    ) { outputUri ->
        if (outputUri == null) {
            status = "Save cancelled"
        } else {
            isWorking = true
            status = "Creating PDF..."
            try {
                createPdf(context, images, outputUri)
                status = "PDF saved successfully ✓"
            } catch (e: Exception) {
                status = "Failed: ${e.message ?: "Unknown error"}"
            } finally {
                isWorking = false
            }
        }
    }

    Surface(modifier = Modifier.fillMaxSize(), color = Color(0xFF0B0D0C)) {
        Column(
            modifier = Modifier.fillMaxSize().padding(24.dp),
            verticalArrangement = Arrangement.Center
        ) {
            Text("__NAME__", color = Color.White, fontSize = 34.sp, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(8.dp))
            Text("Offline Image → PDF", color = Color(0xFF9CA3AF), fontSize = 15.sp)
            Spacer(Modifier.height(30.dp))

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(24.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF151A17))
            ) {
                Column(Modifier.padding(22.dp)) {
                    Text(
                        "Create a PDF from your photos",
                        color = Color.White,
                        fontSize = 19.sp,
                        fontWeight = FontWeight.SemiBold
                    )
                    Spacer(Modifier.height(8.dp))
                    Text(
                        "Runs locally on your phone. No upload required.",
                        color = Color(0xFF9CA3AF)
                    )
                    Spacer(Modifier.height(22.dp))

                    Button(
                        onClick = { picker.launch("image/*") },
                        modifier = Modifier.fillMaxWidth(),
                        enabled = !isWorking,
                        colors = ButtonDefaults.buttonColors(
                            containerColor = Color(0xFF252C27),
                            contentColor = Color.White
                        )
                    ) {
                        Text("SELECT IMAGES", fontWeight = FontWeight.Bold)
                    }

                    Spacer(Modifier.height(12.dp))

                    Button(
                        onClick = { savePdf.launch("images.pdf") },
                        modifier = Modifier.fillMaxWidth(),
                        enabled = images.isNotEmpty() && !isWorking,
                        colors = ButtonDefaults.buttonColors(
                            containerColor = Color(0xFFB7FF3C),
                            contentColor = Color.Black,
                            disabledContainerColor = Color(0xFF3A4637),
                            disabledContentColor = Color(0xFF8B9488)
                        )
                    ) {
                        Text(if (isWorking) "CREATING..." else "CREATE PDF", fontWeight = FontWeight.Bold)
                    }

                    Spacer(Modifier.height(18.dp))
                    Text(
                        status,
                        color = if (status.contains("✓")) Color(0xFFB7FF3C) else Color(0xFFB8C0B8)
                    )

                    if (images.isNotEmpty()) {
                        Spacer(Modifier.height(6.dp))
                        Text("${images.size} page(s) will be created", color = Color(0xFF6F7A71), fontSize = 13.sp)
                    }
                }
            }

            Spacer(Modifier.height(26.dp))
            Text(
                "Ecrin Labs",
                color = Color(0xFF6B7280),
                modifier = Modifier.align(Alignment.CenterHorizontally)
            )
        }
    }
}

@Throws(IOException::class)
fun createPdf(context: Context, images: List<Uri>, outputUri: Uri) {
    if (images.isEmpty()) throw IllegalArgumentException("No images selected")

    val pdf = PdfDocument()
    val pageWidth = 1240
    val pageHeight = 1754
    val margin = 48

    try {
        images.forEachIndexed { index, uri ->
            val bitmap = decodeBitmap(context, uri)
                ?: throw IOException("Could not read image ${index + 1}")

            val pageInfo = PdfDocument.PageInfo.Builder(pageWidth, pageHeight, index + 1).create()
            val page = pdf.startPage(pageInfo)
            drawBitmapFit(page.canvas, bitmap, pageWidth, pageHeight, margin)
            pdf.finishPage(page)

            if (!bitmap.isRecycled) bitmap.recycle()
        }

        context.contentResolver.openOutputStream(outputUri)?.use { out ->
            pdf.writeTo(out)
        } ?: throw IOException("Could not open output file")
    } finally {
        pdf.close()
    }
}

fun decodeBitmap(context: Context, uri: Uri): Bitmap? {
    return context.contentResolver.openInputStream(uri)?.use { stream ->
        BitmapFactory.decodeStream(stream)
    }
}

fun drawBitmapFit(
    canvas: Canvas,
    bitmap: Bitmap,
    pageWidth: Int,
    pageHeight: Int,
    margin: Int
) {
    canvas.drawColor(AndroidColor.WHITE)
    val availableW = (pageWidth - margin * 2).toFloat()
    val availableH = (pageHeight - margin * 2).toFloat()
    val scale = min(availableW / bitmap.width.toFloat(), availableH / bitmap.height.toFloat())

    val drawW = bitmap.width * scale
    val drawH = bitmap.height * scale
    val left = (pageWidth - drawW) / 2f
    val top = (pageHeight - drawH) / 2f

    val src = android.graphics.Rect(0, 0, bitmap.width, bitmap.height)
    val dst = android.graphics.RectF(left, top, left + drawW, top + drawH)
    val paint = Paint(Paint.ANTI_ALIAS_FLAG or Paint.FILTER_BITMAP_FLAG)
    canvas.drawBitmap(bitmap, src, dst, paint)
}
'''.replace("__PKG__", pkg).replace("__NAME__", name)

write(root / "app/src/main/java" / pp / "MainActivity.kt", main_kt)

write(root / "FACTORY_RECIPE.txt", f'''Ecrin App Factory V3
Request: {request}
Recipe: {recipe}
Generated app: {name}
Package: {pkg}
Capabilities:
- Multi-image picker
- Offline image decoding
- Real Android PdfDocument generation
- One image per PDF page
- System save dialog
- No broad storage permission
''')

print("Factory V3 generated a REAL app recipe")
print("Recipe:", recipe)
print("App:", name)
print("Package:", pkg)
