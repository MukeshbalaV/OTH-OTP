import qrcode
import pyotp
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import io

class OTPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OTP QR Code Generator and Verifier")
        self.root.geometry("400x500")
        self.root.configure(bg="#edf0f5")

        self.secret = pyotp.random_base32()
        self.totp = pyotp.TOTP(self.secret, interval=30)

        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20, relief=tk.RAISED, bd=2)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(self.login_frame, text="Login", bg="#ffffff", font=("Helvetica", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        tk.Label(self.login_frame, text="Hello! Let's get started", bg="#ffffff", font=("Helvetica", 12)).grid(row=1, column=0, columnspan=2, pady=(0, 20))

        tk.Label(self.login_frame, text="Username:", bg="#ffffff", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica", 12))
        self.username_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(self.login_frame, text="Password:", bg="#ffffff", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica", 12))
        self.password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.verify_login, bg="#4285F4", fg="white", font=("Helvetica", 12), relief=tk.FLAT)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=(20, 10), ipadx=50)

        self.forgot_password_label = tk.Label(self.login_frame, text="Forgot password?", bg="#ffffff", fg="#4285F4", font=("Helvetica", 12, "underline"))
        self.forgot_password_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        self.login_frame.columnconfigure(1, weight=1)

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "user" and password == "pass":
            self.login_frame.destroy()
            self.setup_otp_selection_frame()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def setup_otp_selection_frame(self):
        self.selection_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20, relief=tk.RAISED, bd=2)
        self.selection_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(self.selection_frame, text="Choose OTP Method:", bg="#ffffff", font=("Helvetica", 14)).pack(pady=10)

        self.qr_button = tk.Button(self.selection_frame, text="QR Code", command=self.setup_qr_code_frame, bg="#34A853", fg="white", font=("Helvetica", 12), relief=tk.FLAT)
        self.qr_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.ussd_button = tk.Button(self.selection_frame, text="USSD", command=self.setup_ussd_frame, bg="#FBBC05", fg="white", font=("Helvetica", 12), relief=tk.FLAT)
        self.ussd_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def setup_qr_code_frame(self):
        self.selection_frame.destroy()

        self.qr_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20, relief=tk.RAISED, bd=2)
        self.qr_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.qr_label = tk.Label(self.qr_frame, bg="#ffffff")
        self.qr_label.pack(pady=10)

        otp_frame = tk.Frame(self.qr_frame, bg="#ffffff")
        otp_frame.pack()

        self.otp_entry = tk.Entry(otp_frame, width=20, font=("Helvetica", 12))
        self.otp_entry.pack(side=tk.LEFT, padx=5)

        self.verify_button = tk.Button(otp_frame, text="Verify OTP", command=self.verify_otp_qr, bg="#4285F4", fg="white", font=("Helvetica", 12), relief=tk.FLAT)
        self.verify_button.pack(side=tk.LEFT, padx=5)

        self.error_label = tk.Label(self.qr_frame, text="", fg="red", bg="#ffffff", font=("Helvetica", 12))
        self.error_label.pack(pady=5)

        self.generate_qr_code()

    def setup_ussd_frame(self):
        self.selection_frame.destroy()

        self.ussd_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20, relief=tk.RAISED, bd=2)
        self.ussd_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(self.ussd_frame, text="Enter USSD Code:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=10)

        self.ussd_entry = tk.Entry(self.ussd_frame, width=30, font=("Helvetica", 12))
        self.ussd_entry.pack(side=tk.LEFT, padx=5)

        self.generate_otp_button = tk.Button(self.ussd_frame, text="Generate OTP", command=self.generate_and_display_otp, bg="#4285F4", fg="white", font=("Helvetica", 12), relief=tk.FLAT)
        self.generate_otp_button.pack(side=tk.LEFT, padx=5)

        self.otp_display_label = tk.Label(self.ussd_frame, text="", bg="#ffffff", font=("Helvetica", 12))
        self.otp_display_label.pack(pady=5)

        otp_input_frame = tk.Frame(self.ussd_frame, bg="#ffffff")
        otp_input_frame.pack()

        self.otp_input_entry = tk.Entry(otp_input_frame, width=20, font=("Helvetica", 12))
        self.otp_input_entry.pack(side=tk.LEFT, padx=5)

        self.otp_verify_button = tk.Button(otp_input_frame, text="Enter OTP", command=self.verify_otp_ussd, bg="#4285F4", fg="white", font=("Helvetica", 12), relief=tk.FLAT)
        self.otp_verify_button.pack(side=tk.LEFT, padx=5)

        self.ussd_error_label = tk.Label(self.ussd_frame, text="", fg="red", bg="#ffffff", font=("Helvetica", 12))
        self.ussd_error_label.pack(pady=5)

    def generate_qr_code(self):
        otp = self.totp.now()
        print(f"Generated OTP: {otp}")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.totp.provisioning_uri("test@example.com", issuer_name="MyApp"))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        with io.BytesIO() as output:
            img.save(output, format="PNG")
            qr_image = Image.open(output)
            qr_image_tk = ImageTk.PhotoImage(qr_image)

        self.qr_label.configure(image=qr_image_tk)
        self.qr_label.image = qr_image_tk

    def generate_and_display_otp(self):
        otp = self.totp.now()
        self.otp_display_label.config(text=f"Generated OTP: {otp}")
        print(f"Generated OTP: {otp}")

    def verify_otp_qr(self):
        otp = self.otp_entry.get()
        if self.totp.verify(otp):
            self.qr_frame.destroy()
            self.show_success_screen()
        else:
            self.error_label.config(text="Invalid OTP, try again")
            print("Invalid OTP entered")
            self.generate_qr_code()

    def verify_otp_ussd(self):
        otp = self.otp_input_entry.get()
        if self.totp.verify(otp):
            self.ussd_frame.destroy()
            self.show_success_screen()
        else:
            self.ussd_error_label.config(text="Invalid OTP, try again")
            print("Invalid OTP entered")
            self.generate_and_display_otp()

    def show_success_screen(self):
        success_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20, relief=tk.RAISED, bd=2)
        success_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(success_frame, text="Login Successful!", bg="#ffffff", font=("Helvetica", 18, "bold")).pack(pady=10)
        tk.Label(success_frame, text="You have successfully logged in using OTP.", bg="#ffffff", font=("Helvetica", 12)).pack(pady=10)

        self.exit_button = tk.Button(success_frame, text="Exit", command=self.root.quit, bg="#4285F4", fg="white", font=("Helvetica", 12), relief=tk.FLAT)
        self.exit_button.pack(pady=20, ipadx=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = OTPApp(root)
    root.mainloop()
