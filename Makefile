PYTHON_FILE=./src/main.py
BIN_FILENAME=./firmware/camera.bin
UPLOAD_PORT?=/dev/tty.usbmodem1234561
SERIAL_PORT?=/dev/tty.usbmodem2101

.PHONY: default upload setup rollback log shell

default: upload

setup: ## Erase flash and then upload the micropython binary
	@echo "Ensure you plug in the board into the USB port"
	@ls /dev/tty.*
	pipenv run esptool.py --chip esp32s3 --port $(SERIAL_PORT) --baud 115200 erase_flash
	pipenv run esptool.py --chip esp32s3 --port $(SERIAL_PORT) write_flash -z 0 $(BIN_FILENAME)

upload: ## Access the serial monitor with rshell
	@ls /dev/tty.*
	@echo "Ensure you plug in the board into the UART port"
	pipenv run rshell cp $(PYTHON_FILE) /pyboard/

rollback:
	@ls /dev/tty.*
	@echo "Ensure you plug in the board into the UART port"
	pipenv run esptool.py --chip esp32s3 --port $(SERIAL_PORT) --baud 115200 erase_flash

log:
	screen $(UPLOAD_PORT) 115200

shell:
	pipenv run rshell -p $(UPLOAD_PORT)
