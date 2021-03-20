################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
F:\eclipse\arduinoPlugin\packages\adafruit\hardware\samd\1.6.4\cores\arduino\TinyUSB\Adafruit_TinyUSB_ArduinoCore\tinyusb\src\portable\dialog\da146xx\dcd_da146xx.c 

C_DEPS += \
.\core\core\TinyUSB\Adafruit_TinyUSB_ArduinoCore\tinyusb\src\portable\dialog\da146xx\dcd_da146xx.c.d 

AR_OBJ += \
.\core\core\TinyUSB\Adafruit_TinyUSB_ArduinoCore\tinyusb\src\portable\dialog\da146xx\dcd_da146xx.c.o 


# Each subdirectory must supply rules for building sources it contributes
core\core\TinyUSB\Adafruit_TinyUSB_ArduinoCore\tinyusb\src\portable\dialog\da146xx\dcd_da146xx.c.o: F:\eclipse\arduinoPlugin\packages\adafruit\hardware\samd\1.6.4\cores\arduino\TinyUSB\Adafruit_TinyUSB_ArduinoCore\tinyusb\src\portable\dialog\da146xx\dcd_da146xx.c
	@echo 'Building file: $<'
	@echo 'Starting C compile'
	"F:\eclipse\arduinoPlugin\packages\adafruit\tools\arm-none-eabi-gcc\9-2019q4/bin/arm-none-eabi-gcc" -mcpu=cortex-m4 -mthumb -c -g -Os -Wall -Wextra -Wno-expansion-to-defined -std=gnu11 -ffunction-sections -fdata-sections -nostdlib --param max-inline-insns-single=500 -MMD -D__SKETCH_NAME__="""CyTracker""" -DF_CPU=120000000L -DARDUINO=10812 -DARDUINO_FEATHER_M4 -DARDUINO_ARCH_SAMD  -D__SAMD51J19A__ -DADAFRUIT_FEATHER_M4_EXPRESS -D__SAMD51__ -DUSB_VID=0x239A -DUSB_PID=0x8022 -DUSBCON -DUSB_CONFIG_POWER=100 "-DUSB_MANUFACTURER=\"Adafruit LLC\"" "-DUSB_PRODUCT=\"Adafruit Feather M4\"" -DUSE_TINYUSB -g "-IF:\eclipse\arduinoPlugin\packages\adafruit\hardware\samd\1.6.4\cores\arduino/TinyUSB" "-IF:\eclipse\arduinoPlugin\packages\adafruit\hardware\samd\1.6.4\cores\arduino/TinyUSB/Adafruit_TinyUSB_ArduinoCore" "-IF:\eclipse\arduinoPlugin\packages\adafruit\hardware\samd\1.6.4\cores\arduino/TinyUSB/Adafruit_TinyUSB_ArduinoCore/tinyusb/src" -D__FPU_PRESENT -DARM_MATH_CM4 -mfloat-abi=hard -mfpu=fpv4-sp-d16 -DENABLE_CACHE  -g -Os  -DVARIANT_QSPI_BAUD_DEFAULT=50000000 "-IF:\eclipse\arduinoPlugin\packages\adafruit\tools\CMSIS\5.4.0/CMSIS/Core/Include/" "-IF:\eclipse\arduinoPlugin\packages\adafruit\tools\CMSIS\5.4.0/CMSIS/DSP/Include/" "-IF:\eclipse\arduinoPlugin\packages\arduino\tools\CMSIS-Atmel\1.2.0/CMSIS/Device/ATMEL/"   -I"F:\eclipse\arduinoPlugin\packages\adafruit\hardware\samd\1.6.4\cores\arduino" -I"F:\eclipse\arduinoPlugin\packages\adafruit\hardware\samd\1.6.4\variants\feather_m4" -I"F:\eclipse-workspace\CyStack\CyTracker\Firmware\Adafruit_SleepyDog" -I"F:\eclipse\arduinoPlugin\packages\adafruit\hardware\samd\1.6.4\libraries\SPI" -I"F:\eclipse\arduinoPlugin\packages\adafruit\hardware\samd\1.6.4\libraries\Wire" -I"F:\eclipse\arduinoPlugin\packages\adafruit\hardware\samd\1.6.4\libraries\Adafruit_ZeroDMA\utility" -I"F:\eclipse\arduinoPlugin\packages\adafruit\hardware\samd\1.6.4\libraries\Adafruit_ZeroDMA" -I"F:\eclipse-workspace\CyTracker\libraries\Adafruit_SleepyDog\utility" -I"F:\eclipse-workspace\CyTracker\libraries\Adafruit_SleepyDog" -I"F:\eclipse-workspace\CyTracker\libraries\RadioHead" -I"F:\eclipse-workspace\CyTracker\libraries\Adafruit_GPS\src" -I"F:\eclipse-workspace\CyStack\CyTracker\Firmware\libraries\CyTrackerSERCOM_Handler" -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -D__IN_ECLIPSE__=1 "$<"   -o "$@"
	@echo 'Finished building: $<'
	@echo ' '


