# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Missions
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from smm_client.geometry import SMMLine, SMMPoi, SMMPolygon

if TYPE_CHECKING:
    from smm_client.assets import SMMAsset, SMMUser
    from smm_client.connection import SMMConnection
    from smm_client.organizations import SMMOrganization
    from smm_client.types import SMMPoint


class SMMMissionOrganization:
    """
    Search Management Map - Organization membership of a Mission
    """

    def __init__(self, mission: SMMMission, organization: SMMOrganization) -> None:
        self.mission = mission
        self.organization = organization

    def set_can_add_organizations(self, *, value: bool) -> bool:
        """
        Set whether this organization can add organizations or not
        """
        response = self.mission.post(f"organizations/{self.organization.id}/", {"add_organization": value})
        return response.status_code == requests.codes["ok"]

    def set_can_add_users(self, *, value: bool) -> bool:
        """
        Set whether this organization can add members or not
        """
        response = self.mission.post(f"organizations/{self.organization.id}/", {"add_user": value})
        return response.status_code == requests.codes["ok"]


class SMMMissionMember:
    """
    Search Management Map - User membership of a Mission
    """

    def __init__(self, mission: SMMMission, user: SMMUser) -> None:
        self.mission = mission
        self.user = user

    def set_is_admin(self, *, value: bool) -> bool:
        """
        Set whether this user is an admin or not
        Admins have all other permissions as well
        """
        response = self.mission.post(f"users/{self.user.id}/", {"admin": value})
        return response.status_code == requests.codes["ok"]

    def set_can_add_organizations(self, *, value: bool) -> bool:
        """
        Set whether this organization can add organizations or not
        """
        response = self.mission.post(f"users/{self.user.id}/", {"add_organization": value})
        return response.status_code == requests.codes["ok"]

    def set_can_add_users(self, *, value: bool) -> bool:
        """
        Set whether this organization can add members or not
        """
        response = self.mission.post(f"users/{self.user.id}/", {"add_user": value})
        return response.status_code == requests.codes["ok"]


class SMMMission:
    """
    Search Management Map - Mission
    """

    def __init__(self, connection: SMMConnection, mission_id: int, name: str) -> None:
        self.connection = connection
        self.id = mission_id
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    def __url_component(self, page: str) -> str:
        return f"/mission/{self.id}/{page}"

    def post(self, page: str, data: object):
        """
        Post data to a specific url in this mission
        """
        return self.connection.post(self.__url_component(page), data)

    def add_member(self, user: SMMUser) -> SMMMissionMember:
        """
        Add a member to this mission
        """
        self.post("users/add/", data={"user": user.username})
        return SMMMissionMember(self, user)

    def add_organization(self, organization: SMMOrganization) -> SMMMissionOrganization:
        """
        Add an organization to this mission
        """
        self.post("organizations/add/", data={"organization": organization.id})
        return SMMMissionOrganization(self, organization)

    def add_asset(self, asset: SMMAsset) -> None:
        """
        Add an asset to this mission
        """
        self.post("assets/", data={"asset": asset.id})

    def remove_asset(self, asset: SMMAsset) -> None:
        """
        Remove an asset from this mission
        """
        self.connection.get(self.__url_component(f"assets/{asset.id}/remove/"))

    def set_asset_command(self, asset: SMMAsset, command: str, reason: str, point: SMMPoint | None = None) -> None:
        """
        Set the command for a specific asset
        """
        data = {
            "asset": asset.id,
            "command": command,
            "reason": reason,
        }
        if point is not None:
            data["latitude"] = point.latitude
            data["longitude"] = point.longitude
        self.post("assets/command/set/", data)

    def close(self) -> None:
        """
        Close this mission
        """
        self.connection.get(self.__url_component("close/"))

    def assets(self, include: str = "active") -> list[str]:
        """
        Get all the assets in this mission

        Use include="removed" to see get all assets that were ever in the mission
        """
        return self.connection.get_json(self.__url_component(f"assets/?include_removed={include == "removed"}"))

    def add_waypoint(self, point: SMMPoint, label: str) -> SMMPoi | None:
        """
        Add a way point to this mission
        """
        results = self.post("data/pois/create/", {"lat": point.lat, "lon": point.lng, "label": label})
        if results.status_code == requests.codes["ok"]:
            json_obj = results.json()
            return SMMPoi(self, json_obj["features"][0]["properties"]["pk"])
        return None

    def _populate_points(self, points: list[SMMPoint], label) -> object:
        """
        Add the points to data
        """
        data = {
            "points": len(points),
            "label": label,
        }
        i = 0
        for point in points:
            data[f"point{i}_lat"] = point.lat
            data[f"point{i}_lng"] = point.lng
            i = i + 1
        return data

    def add_line(self, points: list[SMMPoint], label: str) -> SMMLine | None:
        """
        Add a line to this mission
        """
        data = self._populate_points(points, label)
        results = self.post("data/userlines/create/", data)
        if results.status_code == requests.codes["ok"]:
            json_obj = results.json()
            return SMMLine(self, json_obj["features"][0]["properties"]["pk"])
        return None

    def add_polygon(self, points: list[SMMPoint], label: str) -> SMMPolygon | None:
        """
        Add a polygon to this mission
        """
        data = self._populate_points(points, label)
        results = self.post("data/userpolygons/create/", data)
        if results.status_code == requests.codes["ok"]:
            json_obj = results.json()
            return SMMPolygon(self, json_obj["features"][0]["properties"]["pk"])
        return None
