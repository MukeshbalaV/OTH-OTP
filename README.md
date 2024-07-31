# OTP QR Code Generator and Verifier

## Overview

This project is a desktop application for generating and verifying OTPs using QR codes and USSD codes. The application is built with Python, utilizing the Tkinter library for the GUI, `pyotp` for OTP generation, and `qrcode` for QR code creation.

## Features

- **Login Authentication**: Simple username and password login.
- **OTP Methods**: Choose between QR code and USSD for OTP verification.
- **QR Code Generation**: Generates a QR code for OTP authentication.
- **OTP Verification**: Verify OTPs for both QR code and USSD methods.
- **User Feedback**: Display success messages or errors based on OTP verification results.

## Prerequisites

Ensure you have the following Python packages installed:

- `qrcode`
- `pyotp`
- `Pillow` (PIL)
- `tkinter` (usually included with Python)

You can install the required packages using `pip`:

```bash
pip install qrcode pyotp Pillow
```

## Usage

1. **Run the Application**: Execute the script to launch the application.
    ```bash
    python otp_app.py
    ```

2. **Login**: Enter the username and password (default: `user` / `pass`).

3. **Choose OTP Method**: Select between "QR Code" and "USSD".

4. **QR Code**:
    - A QR code will be generated.
    - Scan the QR code with an OTP app (e.g., Google Authenticator).
    - Enter the OTP from the app to verify.

5. **USSD**:
    - Enter a USSD code and generate an OTP.
    - Enter the OTP displayed to verify.

6. **Successful Login**: If the OTP is valid, you'll see a success message.

## Code Structure

- `OTPApp` class: Handles the application logic and GUI.
- `create_login_frame()`: Sets up the login interface.
- `verify_login()`: Checks the login credentials.
- `setup_otp_selection_frame()`: Allows users to choose OTP method.
- `setup_qr_code_frame()`: Generates and displays a QR code.
- `setup_ussd_frame()`: Handles USSD code entry and OTP generation.
- `generate_qr_code()`: Creates a QR code for OTP.
- `generate_and_display_otp()`: Generates and displays OTP for USSD.
- `verify_otp_qr()`: Verifies OTP for QR code.
- `verify_otp_ussd()`: Verifies OTP for USSD.
- `show_success_screen()`: Displays a success message upon successful login.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or bug fixes.

## Contact

For any questions or issues, please open an issue on the GitHub repository.

