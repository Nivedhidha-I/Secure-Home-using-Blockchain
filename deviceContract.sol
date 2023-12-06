// SPDX-License-Identifier: UNLICENSED
// version of compiler
pragma solidity ^0.8.19;
// creation of contract
contract device {
  // introducing the threshold value of Ultrasonic sensor which defines if anyone in room
  uint public threshold_UDS = 200;
  
  // mapping address of iot set to UDS value
  mapping(address => uint) UDS;
  
  // mapping address of iot set to PIR value
  mapping(address => bool) PIR;
  
  // mapping address of iot set to FAN value
  mapping(address => bytes32) FAN;
  
  // checking if should on the fan
  modifier shouldOnFAN(address id) {
    require(FAN[id] == "OFF" && UDS[id] < threshold_UDS && PIR[id] == true);
    _;
  }
  
  // checking if should on the fan
  modifier shouldOffFAN(address id) {
    require(FAN[id] == "ON" && (UDS[id] >= threshold_UDS || PIR[id] == false));
    _;
  }
  
  // on the fan if it is off and if person is in the room
  function onFAN(address id) external shouldOnFAN(id) {
    FAN[id] = "ON";
  }
  
  // off the fan if it is off and if person is in the room
  function offFAN(address id) external shouldOffFAN(id) {
    FAN[id] = "OFF";
  }
  
  // getting current state of FAN
  function viewFANState(address id) public view returns (bytes32) {
    return FAN[id];
  }
  
}
