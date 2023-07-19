#!/usr/bin/env python3
import json
import sys
import datetime  
import SkyboxAPI
import time
import paho.mqtt.client as mqtt

mqtt_host = "192.168.10.8"
mqtt_port = 1883
mqtt_user = "mqtt"
mqtt_password = "mosquitto"
mqtt_base_topic = "outback_skybox"
temp_json = {}

def on_connect(client, userdata, flags, rc):
    #print("MQTT connected with result code "+str(rc))
    client.will_set(mqtt_base_topic + "/availability","offline", qos=0, retain=False)
    global mqtt_connected
    mqtt_connected = True

def on_disconnect(client, userdata, rc):
    #print("MQTT disconnected with result code "+str(rc))
    global mqtt_connected
    mqtt_connected = False
    
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_message = on_message

client.username_pw_set(username=mqtt_user, password=mqtt_password)
client.connect(mqtt_host, mqtt_port, 60)
client.loop_start()
time.sleep(2)


#this is an example usage of the SkyboxAPI to retrieve and print various metrics
def main(argv=None): 
    # make sure you have enabled remote login in Global Settings -> System -> Remote Security -> Enable Remote Login. 
    s = SkyboxAPI.SkyboxAPI()

    # The web interface will be running on port 3000. you can check your skybox IP address on the skybox in the Global Settings -> Network
    # It will attempt to use the outback default remote access account of username = "I" and password = "skybox"
    # You can change this to a custom userename password like this:
    loginStatus = s.login("http://192.168.10.224:3000","I","sb") 
    # this will log you into the skybox and allow you to perform further inquiries
    # loginStatus = s.login("http://192.168.10.224:3000") 
    # optionally, we can save and print the login status 
    # loginStatus = s.login("http://192.168.1.142:3000") 
    #print(loginStatus)
    
    client.publish(mqtt_base_topic + "/loginstatus",str(loginStatus))
    client.publish(mqtt_base_topic + "/availability","online")

    
    # Lets get the current status and print a few metrics
    while True:
        status = s.getStatus()
        temp_json["battery_state_of_charge"] = float(status["battery_state_of_charge"])
        temp_json["battery_watts"] = float(status["battery_watts"])
        temp_json["battery_voltage"] = float(status["battery_voltage"])
        temp_json["grid_realtime_frequency"] = float(status["grid_realtime_frequency"])
        temp_json["grid_l1_realtime_wattage"] = float(status["grid_l1_realtime_wattage"])
        temp_json["grid_l2_realtime_wattage"] = float(status["grid_l2_realtime_wattage"])
        temp_json["grid_realtime_wattage_sum"] = float(status["grid_realtime_wattage_sum"])
        temp_json["grid_l1_realtime_ac_voltage"] = float(status["grid_l1_realtime_ac_voltage"])
        temp_json["grid_l2_realtime_ac_voltage"] = float(status["grid_l2_realtime_ac_voltage"])
        temp_json["load_realtime_frequency"] = float(status["load_realtime_frequency"])
        temp_json["load_combined_l1_wattage"] = float(status["load_combined_l1_wattage"])
        temp_json["load_combined_l2_wattage"] = float(status["load_combined_l2_wattage"])
        temp_json["load_combined_wattage_sum"] = float(status["load_combined_wattage_sum"])
        temp_json["pv_input_power"] = float(status["pv_input_power"])
        temp_json["pv_kwh_today"] = float(status["pv_kwh_today"])
        temp_json["pv_production_realtime_kw_min"] = float(status["pv_production_realtime_kw_min"])
        temp_json["pv_production_realtime_kw_max"] = float(status["pv_production_realtime_kw_max"])
        temp_json["pv_output_power_dc"] = float(status["pv_output_power_dc"])
        temp_json["pv_bb_input_voltage"] = float(status["pv_bb_input_voltage"])
        temp_json["pv_output_voltage_dc"] = float(status["pv_output_voltage_dc"])
        temp_json["pv_input_current"] = float(status["pv_input_current"])
        temp_json["pv_output_current_dc"] = float(status["pv_output_current_dc"])
        temp_json["grid_l1_kwh_bought_today"] = float(status["grid_l1_kwh_bought_today"])
        temp_json["grid_l2_kwh_bought_today"] = float(status["grid_l2_kwh_bought_today"])
        temp_json["grid_l1_kwh_sold_today"] = float(status["grid_l1_kwh_sold_today"])
        temp_json["grid_l2_kwh_sold_today"] = float(status["grid_l2_kwh_sold_today"])
        temp_json["load_l1_kwh_produced_today"] = float(status["load_l1_kwh_produced_today"])
        temp_json["load_l2_kwh_produced_today"] = float(status["load_l2_kwh_produced_today"])
        temp_json["load_l1_kwh_consumed_today"] = float(status["load_l1_kwh_consumed_today"])
        temp_json["load_l2_kwh_consumed_today"] = float(status["load_l2_kwh_consumed_today"])
        temp_json["load_l1_self_supply_today"] = float(status["load_l1_self_supply_today"])
        temp_json["load_l2_self_supply_today"] = float(status["load_l2_self_supply_today"])
        temp_json["load_total_self_supply_today"] = float(status["load_total_self_supply_today"])
        temp_json["load_l1_ac_voltage"] = float(status["load_l1_ac_voltage"])
        temp_json["load_l1_ac_amps"] = float(status["load_l1_ac_amps"])
        temp_json["load_l1_wattage"] = float(status["load_l1_wattage"])
        temp_json["load_l2_ac_voltage"] = float(status["load_l2_ac_voltage"])
        temp_json["load_l2_ac_amps"] = float(status["load_l2_ac_amps"])
        temp_json["load_l2_wattage"] = float(status["load_l2_wattage"])
        temp_json["load_ac_current_sum"] = float(status["load_ac_current_sum"])
        temp_json["load_wattage_sum"] = float(status["load_wattage_sum"])
        temp_json["load_unprotected_l1_wattage"] = float(status["load_unprotected_l1_wattage"])
        temp_json["load_unprotected_l2_wattage"] = float(status["load_unprotected_l2_wattage"])
        temp_json["load_l1_self_supply"] = float(status["load_l1_self_supply"])
        temp_json["load_l2_self_supply"] = float(status["load_l2_self_supply"])
        temp_json["load_total_self_supply"] = float(status["load_total_self_supply"])
        temp_json["battery_ah_charging_today"] = float(status["battery_ah_charging_today"])
        temp_json["battery_ah_discharging_today"] = float(status["battery_ah_discharging_today"])
        temp_json["battery_kwh_charging_today"] = float(status["battery_kwh_charging_today"])
        temp_json["battery_kwh_discharging_today"] = float(status["battery_kwh_discharging_today"])
        temp_json["battery_dc_bus_power"] = float(status["battery_dc_bus_power"])
        temp_json["battery_dc_bus_voltage"] = float(status["battery_dc_bus_voltage"])
        temp_json["battery_amps"] = float(status["battery_amps"])
        temp_json["battery_dc_bus_current"] = float(status["battery_dc_bus_current"])
        real_json = json.dumps(temp_json)
        #print (real_json)
        #print (status)
        #statusMsg = "PV_WATTS=" + str(float(status["pv_output_power_dc"])) + " PV_VOLTS=" + str(float(status["pv_pmb_voltage"])) + " GRID_WATTS=" + str(float(status["grid_realtime_wattage_sum"])) + " BATT_WATTS=" + str(float(status["battery_watts"])) + " BATT_VOLTS=" + str(float(status["battery_voltage"])) + " BATT_SOC=" + str(float(status["battery_state_of_charge"]))
        #print (statusMsg)
        #statusMsg = "GRID_FREQUENCY=" + str(float(status["grid_realtime_frequency"]))
        #print (statusMsg)
        client.publish(mqtt_base_topic + "/json",str(real_json))
        time.sleep(1)

    # display the status of the pv input
    # the status is a value from 0 to 6
    #print(status['pv_status'])

    # for every 'metric', there is usually a corresponding 'metric_property' which describes the range of values the metric returns.
    # here we can see that 1 means "producing" and 3 means "sleeping"
    #print(status['pv_status_property'])

    #print the load from the load panel
    #print(status['load_combined_wattage_sum'])

    #printing the corresponding property, describes the units etc
    # print(status['load_combined_wattage_sum_property'])

    #print the load from the load panel
    #print(status['inverter_current_status'])

    #printing the corresponding property, describes the units etc
    #print(status['inverter_current_status_property'])

    #get and print the Alerts, these are the red-marked alerts from the skybox graphical interface. 
    # Also note the timestamps are typically in millisecond epoch time (int), so we can convert them to python datetimes if desired
    #for alert in s.getAlerts():
        #print(str(alert["fileIndex"]) + " " + str(datetime.datetime.fromtimestamp(int(alert["Timestamp"])/1000))  + "\t" + alert["Message"])

    #get and print the Notifcations, these are the in the "log" section of the skybox graphical interface
    #for notifcation in s.getNotifications():
        #print(str(notifcation["fileIndex"]) + " " + str(datetime.datetime.fromtimestamp(int(notifcation["Timestamp"])/1000))  + "\t" + notifcation["Message"])

if __name__ == '__main__':
    sys.exit(main())