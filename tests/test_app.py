from app import app, buses, bookings


def client():
    app.config["TESTING"] = True

    bookings.clear()

    for bus in buses:
        bus["available_seats"] = bus["total_seats"]

    return app.test_client()


def test_health():
    test_client = client()

    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_add_booking():
    test_client = client()

    response = test_client.post(
        "/book",
        data={
            "name": "Anushka",
            "phone": "9876543210",
            "bus_id": "1"
        }
    )

    assert response.status_code == 302
    assert len(bookings) == 1
    assert bookings[0]["name"] == "Anushka"
    assert bookings[0]["phone"] == "9876543210"


def test_invalid_booking():
    test_client = client()

    response = test_client.post(
        "/book",
        data={
            "name": "",
            "phone": "9876543210",
            "bus_id": "1"
        }
    )

    assert response.status_code == 400


def test_api_buses():
    test_client = client()

    response = test_client.get("/api/buses")

    assert response.status_code == 200
    assert len(response.json) == 3