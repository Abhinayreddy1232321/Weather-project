import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import requests
from io import BytesIO

class WeatherTracker:
    def __init__(self):
        # Dictionary to store weather data: {city: [temperature, humidity, condition]}
        self.weather_data = {}

    def add_or_update_city(self, city, temperature, humidity, condition):
        """Add or update weather data for a city."""
        self.weather_data[city] = [temperature, humidity, condition]

    def get_city_weather(self, city):
        """Retrieve weather data for a specific city."""
        return self.weather_data.get(city, None)

    def get_all_cities(self):
        """Retrieve all stored city data."""
        return self.weather_data.items()

    def calculate_average_temperature(self):
        """Calculate and return the average temperature across all cities."""
        if not self.weather_data:
            return None
        total_temp = sum(data[0] for data in self.weather_data.values())
        return total_temp / len(self.weather_data)


# Create the GUI
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.tracker = WeatherTracker()
        self.root.title("Weather Tracker")
        self.root.geometry("500x600")
        self.root.configure(bg="#87ceeb")  # Light sky blue background

        # Title Label
        self.title_label = tk.Label(
            root, text="Weather Tracker", font=("Arial", 24, "bold"), bg="#87ceeb", fg="white"
        )
        self.title_label.pack(pady=20)

        # Input Fields for Adding/Updating City
        self.city_label = tk.Label(root, text="City Name:", font=("Arial", 14), bg="#87ceeb")
        self.city_label.pack()
        self.city_entry = tk.Entry(root, font=("Arial", 14), width=20)
        self.city_entry.pack(pady=5)

        self.temp_label = tk.Label(root, text="Temperature (°C):", font=("Arial", 14), bg="#87ceeb")
        self.temp_label.pack()
        self.temp_entry = tk.Entry(root, font=("Arial", 14), width=20)
        self.temp_entry.pack(pady=5)

        self.humidity_label = tk.Label(root, text="Humidity (%):", font=("Arial", 14), bg="#87ceeb")
        self.humidity_label.pack()
        self.humidity_entry = tk.Entry(root, font=("Arial", 14), width=20)
        self.humidity_entry.pack(pady=5)

        self.condition_label = tk.Label(root, text="Condition (e.g., Sunny, Rainy):", font=("Arial", 14), bg="#87ceeb")
        self.condition_label.pack()
        self.condition_entry = tk.Entry(root, font=("Arial", 14), width=20)
        self.condition_entry.pack(pady=5)

        # Buttons
        self.add_button = tk.Button(
            root, text="Add/Update City", font=("Arial", 14), bg="#ffdd57", fg="black", command=self.add_city
        )
        self.add_button.pack(pady=10)

        self.search_label = tk.Label(root, text="Search City Weather:", font=("Arial", 14), bg="#87ceeb")
        self.search_label.pack()
        self.search_entry = tk.Entry(root, font=("Arial", 14), width=20)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(
            root, text="Search City", font=("Arial", 14), bg="#ffdd57", fg="black", command=self.view_city
        )
        self.search_button.pack(pady=10)

        self.all_button = tk.Button(
            root, text="Display All Cities", font=("Arial", 14), bg="#ffdd57", fg="black", command=self.display_all_cities
        )
        self.all_button.pack(pady=10)

        self.avg_button = tk.Button(
            root,
            text="Average Temperature",
            font=("Arial", 14),
            bg="#ffdd57",
            fg="black",
            command=self.calculate_average_temp,
        )
        self.avg_button.pack(pady=10)

        # Weather Icon (Using a default weather icon URL)
        self.icon_image = self.load_weather_icon()
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)
        self.icon_label = tk.Label(root, image=self.icon_photo, bg="#87ceeb")
        self.icon_label.pack(pady=10)

    def load_weather_icon(self):
        """Load a default weather icon from the web."""
        icon_url = "https://www.iconfinder.com/data/icons/weather-forecast-19/64/weather_19-512.png"  # Example weather icon URL
        try:
            response = requests.get(icon_url)
            img_data = response.content
            image = Image.open(BytesIO(img_data))
            return image.resize((100, 100), Image.ANTIALIAS)
        except Exception as e:
            print(f"Error loading icon: {e}")
            # Return a solid color placeholder if the image fails to load
            return Image.new("RGB", (100, 100), color="lightblue")

    def add_city(self):
        city = self.city_entry.get().capitalize()
        try:
            temperature = float(self.temp_entry.get())
            humidity = float(self.humidity_entry.get())
            condition = self.condition_entry.get().capitalize()

            if not city or not condition:
                raise ValueError("City and condition cannot be empty!")

            self.tracker.add_or_update_city(city, temperature, humidity, condition)
            messagebox.showinfo("Success", f"Weather data for {city} added/updated successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def view_city(self):
        city = self.search_entry.get().capitalize()
        data = self.tracker.get_city_weather(city)
        if data:
            temperature, humidity, condition = data
            self.show_weather_window(city, temperature, humidity, condition)
        else:
            messagebox.showwarning("Not Found", f"No weather data available for {city}.")

    def show_weather_window(self, city, temperature, humidity, condition):
        """Display weather data in a visually enhanced window."""
        weather_window = tk.Toplevel(self.root)
        weather_window.title(f"Weather in {city}")
        weather_window.geometry("400x300")
        weather_window.configure(bg="#add8e6")  # Light blue background

        # Weather Info Title
        title_label = tk.Label(weather_window, text=f"Weather in {city}", font=("Arial", 20, "bold"), bg="#add8e6")
        title_label.pack(pady=15)

        # Weather Details
        temp_label = tk.Label(weather_window, text=f"Temperature: {temperature}°C", font=("Arial", 16), bg="#add8e6")
        temp_label.pack(pady=5)

        humidity_label = tk.Label(weather_window, text=f"Humidity: {humidity}%", font=("Arial", 16), bg="#add8e6")
        humidity_label.pack(pady=5)

        condition_label = tk.Label(weather_window, text=f"Condition: {condition}", font=("Arial", 16), bg="#add8e6")
        condition_label.pack(pady=5)

    def display_all_cities(self):
        all_cities = self.tracker.get_all_cities()
        if all_cities:
            details = "\n".join(
                [f"{city}: {data[0]}°C, {data[1]}%, {data[2]}" for city, data in all_cities]
            )
            messagebox.showinfo("All Cities", details)
        else:
            messagebox.showinfo("No Data", "No weather data available!")

    def calculate_average_temp(self):
        avg_temp = self.tracker.calculate_average_temperature()
        if avg_temp is not None:
            messagebox.showinfo("Average Temperature", f"Average Temperature Across All Cities: {avg_temp:.2f}°C")
        else:
            messagebox.showinfo("No Data", "No weather data available to calculate average temperature.")


# Run the GUI Application
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
