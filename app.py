import os
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

buses = [
    {
        "id": 1,
        "number": "BUS-01",
        "route": "Pune Station - MIT-WPU",
        "time": "8:00 AM",
        "total_seats": 40,
        "available_seats": 40
    },
    {
        "id": 2,
        "number": "BUS-02",
        "route": "Kothrud - MIT-WPU",
        "time": "8:15 AM",
        "total_seats": 40,
        "available_seats": 40
    },
    {
        "id": 3,
        "number": "BUS-03",
        "route": "Wakad - MIT-WPU",
        "time": "8:30 AM",
        "total_seats": 40,
        "available_seats": 40
    }
]

bookings = []

COMMIT = os.getenv("RENDER_GIT_COMMIT", "local")[:7]


@app.route("/")
def home():
    return render_template(
        "index.html",
        buses=buses,
        commit=COMMIT
    )


@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name", "").strip()
    bus_id = request.form.get("bus_id", "")

    if not name or not bus_id:
        return "Name and bus are required", 400

    bus = next(
        (bus for bus in buses if bus["id"] == int(bus_id)),
        None
    )

    if not bus:
        return "Bus not found", 404

    if bus["available_seats"] <= 0:
        return "No seats available", 400

    booking = {
        "id": len(bookings) + 1,
        "name": name,
        "bus": bus["number"],
        "route": bus["route"],
        "time": bus["time"]
    }

    bookings.append(booking)
    bus["available_seats"] -= 1

    return redirect("/bookings")


@app.route("/bookings")
def view_bookings():
    return render_template(
        "bookings.html",
        bookings=bookings,
        commit=COMMIT
    )


@app.route("/cancel/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    booking = next(
        (b for b in bookings if b["id"] == booking_id),
        None
    )

    if not booking:
        return "Booking not found", 404

    bookings.remove(booking)

    bus = next(
        (bus for bus in buses if bus["number"] == booking["bus"]),
        None
    )

    if bus:
        bus["available_seats"] += 1

    return redirect("/bookings")


@app.route("/api/buses")
def api_buses():
    return jsonify(buses)


@app.route("/health")
def health():
    return {
        "status": "ok",
        "commit": COMMIT
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )