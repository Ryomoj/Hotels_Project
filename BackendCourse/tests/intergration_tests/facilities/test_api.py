from src.schemas.facilities import FacilityAddSchema


async def test_facilities(ac):
    get_response = await ac.get("/facilities")
    assert get_response.status_code == 200

    new_facility = FacilityAddSchema(title="Огромный мини-бар")
    new_facility_json = {"title": "Огромный мини-бар"}

    post_response = await ac.post(
        "/facilities/facilities",
        json=new_facility_json
    )
    assert post_response.status_code == 200
