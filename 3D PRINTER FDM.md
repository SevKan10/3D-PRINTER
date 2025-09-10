# HƯỚNG DẪN TOÀN DIỆN 3D PRINTER FDM
## Tài liệu Universal cho mọi máy in FDM - By SevKan
### Ngày tạo: 10/09/2025 | Phiên bản: 1.0

---

# 📋 MỤC LỤC

1. [Nguyên tắc cơ bản FDM](#1-nguyên-tắc-cơ-bản-fdm)
2. [Cài đặt Gia tốc (Acceleration)](#2-cài-đặt-gia-tốc-acceleration)
3. [Cài đặt Tốc độ (Speed)](#3-cài-đặt-tốc-độ-speed)
4. [Cài đặt Động cơ và Jerk](#4-cài-đặt-động-cơ-và-jerk)
5. [Cài đặt Z-Offset](#5-cài-đặt-z-offset)
6. [Cài đặt Support](#6-cài-đặt-support)
7. [Cân nhiệt độ Filament](#7-cân-nhiệt-độ-filament)
8. [Troubleshooting](#8-troubleshooting)
9. [Tips nâng cao](#9-tips-nâng-cao)

---

# 1. NGUYÊN TẮC CƠ BẢN FDM

## 🎯 Hiểu về máy in FDM
- **FDM** = Fused Deposition Modeling
- **Nguyên lý**: Đùn nhựa nóng chảy qua layers
- **Factors chính**: Temperature, Speed, Flow, Cooling

## 📏 Thông số máy cần biết trước khi tune

### **Kiểm tra thông số máy:**
```
🔍 THÔNG SỐ CẦN XÁC ĐỊNH:
- Build volume (kích thước in tối đa)
- Nozzle diameter (thường 0.4mm)
- Max speed máy có thể đạt
- Loại hotend (all-metal hay PTFE lined)
- Loại extruder (bowden hay direct drive)
- Firmware (Marlin, Klipper, RepRap, etc.)
- Heated bed có hay không
- Auto bed leveling có hay không
```

### **Baseline settings để bắt đầu:**
```
📊 STARTING POINT CHO MỌI MÁY:
Layer height: 0.2mm (50% nozzle diameter)
Line width: = Nozzle diameter
First layer height: 0.25-0.3mm
Perimeters: 2-3 walls
Top/bottom layers: 4-6 layers
Infill: 10-20%
```

---

# 2. CÀI ĐẶT GIA TỐC (ACCELERATION)

## 🎯 Nguyên tắc Acceleration

### **Acceleration ảnh hưởng gì:**
- **Cao**: In nhanh, có thể rung lắc, ghosting
- **Thấp**: Mượt mà, chất lượng cao, in lâu
- **Rule**: External surfaces luôn thấp nhất

### **Cách xác định Acceleration phù hợp:**

#### **Bước 1: Tìm Max Safe Acceleration**
```
🧪 TEST MAX ACCELERATION:
1. In cube 20x20x20mm với single perimeter
2. Bắt đầu từ 500mm/s²
3. Tăng dần 500mm/s² mỗi lần
4. Dừng khi xuất hiện:
   - Ringing/ghosting
   - Layer shifting
   - Poor surface quality
5. Max safe = giá trị trước khi xuất hiện lỗi
```

#### **Bước 2: Phân chia theo chức năng**
```
📊 ACCELERATION HIERARCHY (% of Max Safe):

External perimeter: 40-60% of max
Internal perimeter: 60-80% of max  
Infill: 80-100% of max
First layer: 20-40% of max
Travel: 100-150% of max (có thể vượt)
Top surface: 40-60% of max

VÍ DỤ: Max safe = 3000mm/s²
- External: 1200-1800mm/s²
- Internal: 1800-2400mm/s²
- Infill: 2400-3000mm/s²
- First layer: 600-1200mm/s²
- Travel: 3000-4500mm/s²
```

### **Acceleration theo loại máy:**

| **Loại máy** | **Max Safe Range** | **Lưu ý** |
|--------------|-------------------|-----------|
| **Bed slinger** (Ender 3, etc.) | 800-2000mm/s² | Bed di chuyển Y, hạn chế |
| **CoreXY** (Voron, etc.) | 3000-8000mm/s² | Bed cố định, rất nhanh |
| **Cartesian** (Prusa i3) | 1500-4000mm/s² | Cân bằng tốt |
| **Delta** | 1000-3000mm/s² | Phức tạp, cần tune |
| **H-Bot** | 2000-5000mm/s² | Tương tự CoreXY |

---

# 3. CÀI ĐẶT TỐC ĐỘ (SPEED)

## 🎯 Nguyên tắc Speed Tuning

### **Speed Hierarchy (từ chậm đến nhanh):**
1. **First layer** - Chậm nhất (adhesion)
2. **External perimeter** - Chậm (surface)
3. **Top surface** - Chậm (aesthetics)
4. **Bridges** - Trung bình (stability)
5. **Internal perimeter** - Nhanh (cấu trúc)
6. **Solid infill** - Nhanh (strength)
7. **Sparse infill** - Nhanh nhất (ẩn)
8. **Travel** - Rất nhanh (không in)

### **Cách tìm Max Speed cho máy:**

#### **Test Maximum Speed:**
```
🧪 SPEED TESTING:

1. In single wall cylinder:
   - Diameter: 20mm, Height: 30mm
   - Wall thickness: 1 perimeter
   - No top, no bottom

2. Test speeds tăng dần:
   - Start: 20mm/s
   - Increment: 10mm/s mỗi 5mm height
   - Continue until failure

3. Failure signs:
   - Under-extrusion
   - Layer gaps
   - Poor surface finish
   - Extruder skipping

4. Max usable = 80% of failure speed
```

### **Speed Guidelines theo nozzle size:**

| **Nozzle** | **Ext. Perim** | **Int. Perim** | **Infill** | **Travel** |
|------------|---------------|---------------|------------|------------|
| **0.2mm** | 15-30mm/s | 25-50mm/s | 40-80mm/s | 100-150mm/s |
| **0.4mm** | 30-80mm/s | 50-150mm/s | 80-200mm/s | 150-250mm/s |
| **0.6mm** | 40-100mm/s | 70-180mm/s | 100-250mm/s | 200-300mm/s |
| **0.8mm** | 50-120mm/s | 80-200mm/s | 120-300mm/s | 250-350mm/s |

### **Speed theo layer height:**

| **Layer Height** | **Speed Multiplier** | **Lý do** |
|------------------|---------------------|-----------|
| **0.1mm** | 0.6-0.8x | Cần thời gian để layer bond |
| **0.15mm** | 0.8-0.9x | Balance tốt |
| **0.2mm** | 1.0x (base) | Standard reference |
| **0.25mm** | 1.1-1.2x | Nhiều plastic hơn |
| **0.3mm** | 1.2-1.4x | Nhanh nhất |

---

# 4. CÀI ĐẶT ĐỘNG CƠ VÀ JERK

## ⚙️ Jerk Settings

### **Hiểu về Jerk:**
- **Jerk** = Tốc độ thay đổi tức thời (mm/s)
- **Cao**: Movements sắc, có thể rung
- **Thấp**: Mượt mà hơn, chậm hơn
- **0**: Disable jerk (dùng acceleration cho mọi thay đổi)

### **Jerk Guidelines:**

#### **Cách test Jerk tối ưu:**
```
🧪 JERK TESTING:

1. In cube với sharp corners
2. Start với jerk thấp:
   - X/Y: 5mm/s
   - Z: 0.5mm/s  
   - E: 2mm/s

3. Tăng dần và quan sát:
   - Too low: Rounded corners, slow
   - Too high: Overshoot, ringing
   - Optimal: Sharp corners, no artifacts

4. Typical ranges:
   - Light machines: 5-12mm/s
   - Heavy machines: 8-20mm/s
   - Delta: 10-30mm/s
```

### **Jerk theo kiểu máy:**

| **Kiểu máy** | **X/Y Jerk** | **Z Jerk** | **E Jerk** | **Ghi chú** |
|--------------|-------------|-----------|-----------|-------------|
| **Bed slinger** | 5-10mm/s | 0.3-0.8mm/s | 2-5mm/s | Y-axis limited |
| **CoreXY** | 8-20mm/s | 0.5-2mm/s | 3-8mm/s | Very capable |
| **Cartesian** | 6-15mm/s | 0.4-1.2mm/s | 2-6mm/s | Balanced |
| **Delta** | 10-30mm/s | 0.5-2mm/s | 3-10mm/s | Different dynamics |

## 🔧 Linear Advance / Pressure Advance

### **Cho Marlin (Linear Advance):**
```gcode
📐 LINEAR ADVANCE TUNING:

1. Enable trong Marlin: #define LIN_ADVANCE
2. Test values: 0.0 - 2.0
3. G-code: M900 K[value]
4. Typical values:
   - Bowden: 0.3-1.5
   - Direct Drive: 0.02-0.2
```

### **Cho Klipper (Pressure Advance):**
```gcode
📐 PRESSURE ADVANCE TUNING:

1. Test command: SET_PRESSURE_ADVANCE ADVANCE=[value]
2. Test range: 0.0-0.1 for direct, 0.02-0.8 for bowden
3. Add to config: pressure_advance: [optimal_value]
```

---

# 5. CÀI ĐẶT Z-OFFSET

## 📏 Z-Offset Universal Methods

### **Method 1: Paper Test**
```
📋 PAPER TEST (Universal):

1. Heat bed to printing temp
2. Home all axes
3. Move nozzle to center of bed
4. Slide paper (A4 = ~0.1mm) giữa nozzle và bed
5. Adjust Z until:
   ✅ Paper has slight drag
   ✅ Can pull out but with resistance
   ✅ Not too tight, not too loose
6. Note Z position = your Z-offset
```

### **Method 2: First Layer Calibration**
```
🎯 FIRST LAYER SIGNS:

❌ TOO HIGH (more negative Z-offset needed):
- Lines don't stick together
- Visible gaps between lines
- Poor bed adhesion
- Easy to remove first layer

✅ PERFECT:
- Lines stick together smoothly
- Slight squish, uniform width
- Good bed adhesion
- Cannot easily separate lines

❌ TOO LOW (less negative Z-offset needed):
- Lines too flat/transparent
- Nozzle scratching bed
- Over-wide extrusion
- Difficult nozzle movement
```

### **Z-Offset theo build surface:**

| **Surface** | **Typical Range** | **Characteristics** |
|-------------|------------------|-------------------|
| **Glass** | -0.05 to -0.20mm | Needs adhesion aid |
| **PEI Smooth** | -0.05 to -0.15mm | Excellent for PLA |
| **PEI Textured** | -0.10 to -0.25mm | Deeper offset needed |
| **BuildTak** | -0.08 to -0.18mm | Good general purpose |
| **Blue tape** | -0.05 to -0.12mm | Classic budget option |

---

# 6. CÀI ĐẶT SUPPORT

## 🏗️ Support Strategy Universal

### **Khi nào cần support:**
- **Overhang > 45°**: Luôn cần
- **Overhang 30-45°**: Tùy material và cooling
- **Bridges > nozzle×50**: Cần support
- **Islands floating**: Luôn cần

### **Support Settings cho Easy Removal:**

#### **Basic Settings:**
```
🔧 SUPPORT CƠ BẢN:
Support threshold: 45° (bắt đầu từ đây)
Support density: 15-20% (đủ mạnh, dễ gỡ)
Support pattern: Lines (dễ gỡ nhất)
Support speed: 60-80% of perimeter speed
```

#### **Interface Settings (QUAN TRỌNG!):**
```
🎯 INTERFACE SETTINGS:
Top interface layers: 3-4 layers
Bottom interface layers: 2-3 layers
Interface pattern: Lines hoặc Rectilinear
Interface spacing: 0.4-0.6mm
Interface density: 70-90%
```

#### **Distance Settings:**
```
📏 DISTANCE SETTINGS:
Top Z distance: 0.2-0.3mm (key cho dễ gỡ!)
Bottom Z distance: 0.15-0.25mm
XY distance: 0.4-0.8mm
Support expansion: 0mm (không mở rộng)
```

### **Support theo loại máy:**

| **Máy type** | **Top Z-distance** | **XY distance** | **Lưu ý** |
|--------------|-------------------|-----------------|-----------|
| **Precise (Prusa, etc.)** | 0.2-0.25mm | 0.4-0.5mm | Chính xác cao |
| **Budget (Ender, etc.)** | 0.25-0.3mm | 0.5-0.7mm | Compensate tolerance |
| **Large format** | 0.3-0.4mm | 0.6-0.8mm | Thermal expansion |
| **High speed** | 0.25-0.35mm | 0.5-0.6mm | Dynamic effects |

---

# 7. CÂN NHIỆT ĐỘ FILAMENT

## 🌡️ Temperature Tuning Universal

### **Nhiệt độ chuẩn theo material:**

| **Material** | **Nozzle Range** | **Bed Range** | **Cooling** | **Lưu ý** |
|--------------|------------------|---------------|-------------|-----------|
| **PLA** | 190-220°C | 50-60°C | 100% | Dễ nhất |
| **PLA+** | 205-225°C | 60-70°C | 80-100% | Bền hơn PLA |
| **PETG** | 220-250°C | 70-85°C | 30-50% | Trong suốt |
| **ABS** | 230-260°C | 90-110°C | 0-30% | Cần enclosure |
| **TPU** | 200-230°C | 30-50°C | 20-50% | Flexible |
| **Wood Fill** | 180-220°C | 50-70°C | 50-80% | Tránh burn |

### **Temperature Testing Method:**

#### **Temperature Tower Test:**
```
🧪 NHIỆT ĐỘ TOWER:

1. Download temperature tower model
2. Set layer-based temperature changes:
   - Mỗi 20 layers giảm 5°C
   - Start: Max temp của material
   - End: Min temp của material

3. G-code for layer changes:
   ;LAYER_CHANGE
   {if layer_num == 20}M104 S[temp-5]{endif}
   {if layer_num == 40}M104 S[temp-10]{endif}
   [continue pattern]

4. Evaluate best section:
   ✅ Smooth surface
   ✅ Good layer adhesion  
   ✅ Minimal stringing
   ✅ No under-extrusion
```

### **Temperature Fine-tuning:**

#### **Environmental adjustments:**
```
🌡️ ĐIỀU CHỈNH THEO MÔI TRƯỜNG:

Mùa đông (Lạnh):
- Nozzle: +5-10°C
- Bed: +5°C
- Cooling: -10-20%

Mùa hè (Nóng):  
- Nozzle: -5°C
- Bed: standard
- Cooling: +10-20%

Phòng có gió:
- Nozzle: +5-8°C
- Bed: +5°C
- Cooling: -20%

Độ ẩm cao:
- Nozzle: +5°C
- Dry filament trước
```

#### **Speed-based temperature:**
```
🏃 NHIỆT ĐỘ THEO TỐC ĐỘ:

Slow (≤40mm/s): Base temperature
Medium (40-80mm/s): Base + 5°C
Fast (80-150mm/s): Base + 10-15°C
Very fast (150mm/s+): Base + 15-20°C

Lý do: Compensate cho reduced melt time
```

---

# 8. TROUBLESHOOTING

## 🔧 Common Issues Universal

### **Print Quality Issues:**

| **Vấn đề** | **Triệu chứng** | **Nguyên nhân thường gặp** | **Giải pháp** |
|------------|----------------|---------------------------|---------------|
| **Stringing** | Plastic threads | Temp cao, retraction kém | Giảm temp, tăng retraction |
| **Layer shifting** | Model bị lệch | Belt lỏng, speed cao | Căng belt, giảm speed |
| **Warping** | Góc cong lên | Cooling nhanh, bed thấp | Tăng bed temp, giảm cooling |
| **Under-extrusion** | Gaps trong layer | Temp thấp, clog, flow thấp | Tăng temp, clean nozzle |
| **Over-extrusion** | Blobs, rough surface | Temp cao, flow cao | Giảm temp, giảm flow |
| **Poor adhesion** | Không dính bed | Z-offset cao, bed lạnh | Giảm Z-offset, tăng bed |

### **Support Issues:**

| **Vấn đề** | **Mô tả** | **Fix** |
|------------|-----------|---------|
| **Support dính chặt** | Khó gỡ support | Tăng Top Z-distance |
| **Support gãy** | Support collapse | Tăng density, giảm speed |
| **Overhang xấu** | Surface không đẹp | Tăng interface layers |
| **Quá nhiều support** | Waste material | Tăng threshold angle |

### **Temperature Problems:**

| **Triệu chứng** | **Likely cause** | **Solution** |
|----------------|------------------|--------------|
| **Clicking extruder** | Temp thấp hoặc clog | Tăng temp, clear nozzle |
| **Oozing** | Temp cao | Giảm temp, tăng retraction |
| **Poor bridging** | Cooling kém | Tăng cooling, giảm speed |
| **Layer gaps** | Temp thấp | Tăng temp, check flow |

---

# 9. TIPS NÂNG CAO

## 🎯 Optimization Strategies

### **Profile Development:**
```
📊 TẠO PROFILE SYSTEM:

1. BASE PROFILES:
   - Quality: Slow, high detail
   - Balanced: Good speed/quality ratio  
   - Speed: Fast prototyping
   - Detailed: Maximum resolution

2. MATERIAL PROFILES:
   - Mỗi material có temperature riêng
   - Cooling settings riêng
   - Retraction settings riêng

3. MACHINE PROFILES:
   - Chuẩn cho từng máy cụ thể
   - Max safe speeds
   - Acceleration limits
```

### **Calibration Schedule:**
```
🗓️ LỊCH CALIBRATION:

HÀNG TUẦN:
- Bed leveling check
- First layer test
- Visual inspection

HÀNG THÁNG:  
- E-steps verification
- Temperature tower test
- Retraction tuning

HÀNG QUÝ:
- Full system calibration
- Belt tension check
- Linear advance tuning
- Flow rate calibration
```

### **Advanced Techniques:**

#### **Adaptive Layer Heights:**
```
📏 ADAPTIVE LAYERS:
- Curved surfaces: Thinner layers
- Flat surfaces: Thicker layers
- Detail areas: Fine resolution
- Support areas: Coarse layers
```

#### **Variable Speed Printing:**
```
🏃 VARIABLE SPEED:
- External perimeters: Slow for quality
- Infill: Fast for efficiency  
- Overhangs: Very slow for stability
- Travel: Maximum speed
```

#### **Advanced Support:**
```
🏗️ SMART SUPPORT:
- Tree support cho organic shapes
- Custom support cho specific areas
- Support painting cho precision
- Support modifiers cho optimization
```

## 🔬 Testing and Validation

### **Test Models:**
```
🧪 ESSENTIAL TEST PRINTS:

Calibration:
- Calibration cube (dimensional)
- Temperature tower (optimal temp)
- Retraction tower (stringing)
- Overhang test (cooling/support)

Quality:
- Benchy boat (overall quality)
- All-in-one test (comprehensive)
- Bridge test (bridging capability)
- Fine detail test (resolution)
```

### **Measurement Tools:**
```
🔧 TOOLS CẦN CÓ:
Essential:
- Digital calipers
- 0.1mm feeler gauges  
- Small ruler/scale

Advanced:
- Micrometer
- Surface roughness gauge
- Digital thermometer
- Oscilloscope (advanced)
```

## 💡 Pro Tips

### **Material Storage:**
```
💾 BẢO QUẢN FILAMENT:
- Vacuum bags với silica gel
- Airtight containers
- Temperature/humidity monitoring
- FIFO rotation system
```

### **Maintenance:**
```
🛠️ BẢO TRÌ ĐỊNH KỲ:
Daily: Clean bed, check filament
Weekly: Lubricate rails, check belts
Monthly: Deep clean, calibrate
Quarterly: Replace wear parts
```

### **Documentation:**
```
📝 GHI CHÉP:
- Settings cho từng material
- Successful print parameters
- Problem và solutions
- Modification history
```

---

## 🎯 KẾT LUẬN

### **Key Principles:**
1. **Start conservative**, tăng dần performance
2. **Test systematically** với small models
3. **Document everything** cho future reference
4. **Understand your machine** limitations
5. **Material-specific tuning** là critical

### **Success Formula:**
```
🏆 THÀNH CÔNG = 
   Proper Calibration + 
   Appropriate Settings + 
   Quality Materials + 
   Regular Maintenance +
   Systematic Testing
```

### **Remember:**
- **Mọi máy đều khác nhau** - cần tune riêng
- **Environment matters** - nhiệt độ, độ ẩm ảnh hưởng
- **Quality takes time** - đừng rush process
- **Documentation saves time** - ghi chép settings
- **Practice makes perfect** - in nhiều để hiểu máy

---

**🎉 CHÚC BẠN IN ẤN THÀNH CÔNG VỚI MỌI MÁY FDM! 🎉**

---
*Tài liệu này được tạo bởi SevKan cho cộng đồng 3D printing*
*Version 1.0 - 2025/09/10*