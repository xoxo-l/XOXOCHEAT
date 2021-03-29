from keyboard import is_pressed
from Utils import time
from API.entity import *
from math import *

from offsets import *
from ctypes import *
from Process.Structures import Vector3, BoneMatrix
import vectormath as vectors

from rich import print

def calc_distance(current_x, current_y, new_x, new_y):
    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    if distancex < 0.0:
        distancex = -distancex
 
    distancey = new_y - current_y
    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    if distancey < 0.0:
        distancey = -distancey
    return distancex, distancey
def checkangles(x, y):
    if x > 89:
        return False
    elif x < -89:
        return False
    elif y > 360:
        return False
    elif y < -360:
        return False
    else:
        return True
def normalize(angle_x, angle_y):
    if angle_x > 89:
        angle_x -= 360
    if angle_x < -89:
        angle_x += 360
    if angle_y > 180:
        angle_y -= 360
    if angle_y < -180:
        angle_y += 360
    return angle_x, angle_y

def distance(player, enemy):
    diff = vectors.Vector3(0.0, 0.0, 0.0)
    diff.x = enemy.x - player.x
    diff.y = enemy.y - player.y
    diff.z = enemy.z - player.z

    distance = sqrt(
      diff.x ** 2 +
      diff.y ** 2 +
      diff.z ** 2
    )

    return abs(distance)

def calcangle(player_pos, entity_pos):
    try:
        delta_x = player_pos.x - entity_pos.x
        delta_y = player_pos.y - entity_pos.y
        delta_z = player_pos.z - entity_pos.z
        hyp = sqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z)
        x = atan(delta_z / hyp) * 180 / pi
        y = atan(delta_y / delta_x) * 180 / pi
        if delta_x >= 0.0:
            y += 180.0
        return x, y
    except:
        pass

def main(csgo):
  head = 8

  while 1:
    player = Player()
    closest = None
    closest_dist = 999999999999999
    for entity in Entity.get_valid():
      if entity.is_valid and player.is_valid and entity.team != player.team:
        enemy_head_pos = entity.get_bone_pos(head)
        player_pos = player.pos
        dist = distance(player_pos, enemy_head_pos)
        if dist < closest_dist:
          closest_dist = dist
          closest = entity

    if closest != None and closest.is_valid and closest.spotted_by_mask:
      enemy_head_pos = closest.get_bone_pos(head)
      player_pos = player.pos
      x, y = calcangle(player_pos, enemy_head_pos)
      while not checkangles(x, y):
        x, y = normalize(x, y)
      player.aim = Vector3(x, y, 0.0)

    time.sleep(1)
