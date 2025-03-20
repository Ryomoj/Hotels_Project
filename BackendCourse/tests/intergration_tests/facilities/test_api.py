async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    res = response.json()
    assert "data" in res
    assert isinstance(res, dict)


async def test_post_facilities(ac):
    facility_title = "Огромный мини-бар"
    new_facility_json = {"title": "Огромный мини-бар"}

    response = await ac.post("/facilities/facilities", json=new_facility_json)
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["data"]["title"] == facility_title
    assert "data" in res
