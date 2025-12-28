#!/usr/bin/env python3
"""
Mini test for broker time sync
Run this on any machine to test sync with the time server
"""

import paho.mqtt.client as mqtt
import json
import time
import threading

class TimeTestClient:
    def __init__(self, client_id, broker_host, broker_port=1883):
        self.client_id = client_id
        self.broker_host = broker_host
        self.broker_port = broker_port
        
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        self._time_response = None
        self._time_event = threading.Event()
        self._time_offset = 0
        
        self.connected = False
    
    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print(f"[{self.client_id}] Connected to broker")
            client.subscribe("time/response")
            self.connected = True
        else:
            print(f"[{self.client_id}] Connection failed: {reason_code}")
    
    def _on_message(self, client, userdata, msg):
        if msg.topic == "time/response":
            try:
                response = json.loads(msg.payload.decode())
                if response.get("requester") == self.client_id:
                    self._time_response = response.get("broker_time")
                    self._time_event.set()
            except Exception as e:
                print(f"[{self.client_id}] Error parsing response: {e}")
    
    def sync_time(self, timeout=2.0):
        """Sync with broker and return offset + round trip time"""
        self._time_event.clear()
        self._time_response = None
        
        local_before = time.time()
        
        request = {"requester": self.client_id}
        self.client.publish("time/request", json.dumps(request))
        
        if self._time_event.wait(timeout):
            local_after = time.time()
            broker_time = self._time_response
            
            local_mid = (local_before + local_after) / 2
            self._time_offset = broker_time - local_mid
            
            rtt_ms = (local_after - local_before) * 1000
            offset_ms = self._time_offset * 1000
            
            return offset_ms, rtt_ms
        else:
            return None, None
    
    def get_broker_time(self):
        """Get broker time using stored offset"""
        return time.time() + self._time_offset
    
    def start(self):
        self.client.connect(self.broker_host, self.broker_port, 60)
        self.client.loop_start()
        
        # Wait for connection
        for _ in range(10):
            if self.connected:
                break
            time.sleep(0.1)
    
    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()


def main():
    import sys
    
    # Get broker IP from command line or use default
    broker_ip = sys.argv[1] if len(sys.argv) > 1 else "192.168.1.84"
    client_id = sys.argv[2] if len(sys.argv) > 2 else "test_client"
    
    print(f"=" * 60)
    print(f"Time Sync Test")
    print(f"=" * 60)
    print(f"Broker: {broker_ip}")
    print(f"Client ID: {client_id}")
    print(f"=" * 60)
    
    client = TimeTestClient(client_id, broker_ip)
    client.start()
    
    if not client.connected:
        print("ERROR: Could not connect to broker")
        return
    
    print("\nRunning 5 sync tests...\n")
    
    offsets = []
    rtts = []
    
    for i in range(5):
        time.sleep(0.5)  # Small delay between tests
        
        offset_ms, rtt_ms = client.sync_time()
        
        if offset_ms is not None:
            offsets.append(offset_ms)
            rtts.append(rtt_ms)
            print(f"Test {i+1}: Offset = {offset_ms:+.2f}ms, RTT = {rtt_ms:.2f}ms")
        else:
            print(f"Test {i+1}: TIMEOUT - Is time server running?")
    
    if offsets:
        print(f"\n" + "=" * 60)
        print(f"Results:")
        print(f"  Avg Offset: {sum(offsets)/len(offsets):+.2f}ms")
        print(f"  Avg RTT:    {sum(rtts)/len(rtts):.2f}ms")
        print(f"  Min RTT:    {min(rtts):.2f}ms")
        print(f"  Max RTT:    {max(rtts):.2f}ms")
        print(f"=" * 60)
        
        # Compare local vs broker time
        print(f"\nTime Comparison:")
        print(f"  Local time:  {time.time():.3f}")
        print(f"  Broker time: {client.get_broker_time():.3f}")
        print(f"  Difference:  {client._time_offset*1000:+.2f}ms")
    
    client.stop()
    print("\nDone.")


if __name__ == "__main__":
    main()