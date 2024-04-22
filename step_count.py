import paho.mqtt.client as mqtt
import time

# MQTT Broker (Server) Details
mqtt_broker_ip = "192.168.227.90"
mqtt_topic = "thala"
mqtt_topic_two = "thalatwo"
mqtt_step_topic = "step"

# Step count variables initialization for each shoe
step_count_total = 0

# Previous force values for each shoe
previous_force_shoe_one = 0
previous_force_shoe_two = 0

# Force buffers for each shoe
force_buffer_shoe_one = [0, 0]  # Buffer to store last 2 force values for shoe one
force_buffer_shoe_two = [0, 0]  # Buffer to store last 2 force values for shoe two

# Cooldown period (in seconds) for each shoe
cooldown_period_shoe_one = 1
cooldown_period_shoe_two = 1

# Timestamps for the last step for each shoe
last_step_time_shoe_one = 0
last_step_time_shoe_two = 0

# Callback function to process incoming MQTT messages
def on_message(client, userdata, msg):
    global step_count_total
    global previous_force_shoe_one
    global previous_force_shoe_two
    global force_buffer_shoe_one
    global force_buffer_shoe_two
    global last_step_time_shoe_one
    global last_step_time_shoe_two

    if msg.topic == mqtt_topic:
        force_shoe_one = float(msg.payload)

        # Update force buffer for shoe one
        force_buffer_shoe_one.pop(0)
        force_buffer_shoe_one.append(force_shoe_one)

        # Condition to check for step for shoe one
        if (force_shoe_one > 6.5) and any(value < 6.5 for value in force_buffer_shoe_one) \
                and (time.time() - last_step_time_shoe_one > cooldown_period_shoe_one):
            step_count_total += 1
            last_step_time_shoe_one = time.time()
            print("Step detected for shoe one. Step count:", step_count_total)

    elif msg.topic == mqtt_topic_two:
        force_shoe_two = float(msg.payload)

        # Update force buffer for shoe two
        force_buffer_shoe_two.pop(0)
        force_buffer_shoe_two.append(force_shoe_two)

        # Condition to check for step for shoe two
        if (force_shoe_two >1.9) and any(value < 1.9 for value in force_buffer_shoe_two) \
                and (time.time() - last_step_time_shoe_two > cooldown_period_shoe_two):
            step_count_total += 1
            last_step_time_shoe_two = time.time()
            print("Step detected for shoe two. Step count:", step_count_total)

    # Publish step count value for both shoes to the "step" topic
    client.publish(mqtt_step_topic, payload=str(step_count_total), qos=0, retain=False)

# Create MQTT client instance
client = mqtt.Client()

# Assign callback function to process incoming messages
client.on_message = on_message

# Connect to MQTT broker
client.connect(mqtt_broker_ip)

# Subscribe to MQTT topics
client.subscribe(mqtt_topic)
client.subscribe(mqtt_topic_two)

# Loop to process incoming messages
client.loop_forever()
