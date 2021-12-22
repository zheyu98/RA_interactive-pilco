// Auto-generated. Do not edit!

// (in-package dcsc_fpga.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let MopsActuators = require('../msg/MopsActuators.js');

//-----------------------------------------------------------


//-----------------------------------------------------------

class MopsWriteRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.actuators = null;
    }
    else {
      if (initObj.hasOwnProperty('actuators')) {
        this.actuators = initObj.actuators
      }
      else {
        this.actuators = new MopsActuators();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MopsWriteRequest
    // Serialize message field [actuators]
    bufferOffset = MopsActuators.serialize(obj.actuators, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MopsWriteRequest
    let len;
    let data = new MopsWriteRequest(null);
    // Deserialize message field [actuators]
    data.actuators = MopsActuators.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 25;
  }

  static datatype() {
    // Returns string type for a service object
    return 'dcsc_fpga/MopsWriteRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9cf6fa7d5fe2d1e423e960795833a766';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    dcsc_fpga/MopsActuators actuators
    
    ================================================================================
    MSG: dcsc_fpga/MopsActuators
    uint8 digital_outputs
    float64 voltage0
    float64 voltage1
    float64 timeout
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new MopsWriteRequest(null);
    if (msg.actuators !== undefined) {
      resolved.actuators = MopsActuators.Resolve(msg.actuators)
    }
    else {
      resolved.actuators = new MopsActuators()
    }

    return resolved;
    }
};

class MopsWriteResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.success = null;
      this.message = null;
    }
    else {
      if (initObj.hasOwnProperty('success')) {
        this.success = initObj.success
      }
      else {
        this.success = false;
      }
      if (initObj.hasOwnProperty('message')) {
        this.message = initObj.message
      }
      else {
        this.message = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MopsWriteResponse
    // Serialize message field [success]
    bufferOffset = _serializer.bool(obj.success, buffer, bufferOffset);
    // Serialize message field [message]
    bufferOffset = _serializer.string(obj.message, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MopsWriteResponse
    let len;
    let data = new MopsWriteResponse(null);
    // Deserialize message field [success]
    data.success = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [message]
    data.message = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.message);
    return length + 5;
  }

  static datatype() {
    // Returns string type for a service object
    return 'dcsc_fpga/MopsWriteResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '937c9679a518e3a18d831e57125ea522';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool success
    string message
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new MopsWriteResponse(null);
    if (msg.success !== undefined) {
      resolved.success = msg.success;
    }
    else {
      resolved.success = false
    }

    if (msg.message !== undefined) {
      resolved.message = msg.message;
    }
    else {
      resolved.message = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: MopsWriteRequest,
  Response: MopsWriteResponse,
  md5sum() { return 'e4d7c08e31b1435de7c05d537862ef59'; },
  datatype() { return 'dcsc_fpga/MopsWrite'; }
};
