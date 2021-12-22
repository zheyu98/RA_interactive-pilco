#!/home/zheyu/anaconda3/envs/RA/bin/python
import rospy
import numpy as np
import tensorflow as tf
import threading
import os
import gym
from tensorflow_probability import bijectors as tfb
import gpflow
import time
import random as rand
import matplotlib.pyplot as plt
from pynput.keyboard import Key, Listener, Controller, KeyCode
from pilco.models import PILCO
from pilco.controllers import RbfController, LinearController
from pilco.rewards import ExponentialReward
from gpflow import set_trainable
from dcsc_fpga.srv import MopsWrite, MopsWriteRequest
from dcsc_fpga.msg import MopsSensors

print(MopsWriteRequest)
