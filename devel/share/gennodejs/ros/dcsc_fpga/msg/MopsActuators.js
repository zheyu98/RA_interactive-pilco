// Auto-generated. Do not edit!

// (in-package dcsc_fpga.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class MopsActuators {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.digital_outputs = null;
      this.voltage0 = null;
      this.voltage1 = null;
      this.timeout = null;
    }
    else {
      if (initObj.hasOwnProperty('digital_outputs')) {
        this.digital_outputs = initObj.digital_outputs
      }
      else {
        this.digital_outputs = 0;
      }
      if (initObj.hasOwnProperty('voltage0')) {
        this.voltage0 = initObj.voltage0
      }
      else {
        this.voltage0 = 0.0;
      }
      if (initObj.hasOwnProperty('voltage1')) {
        this.voltage1 = initObj.voltage1
      }
      else {
        this.voltage1 = 0.0;
      }
      if (initObj.hasOwnProperty('timeout')) {
        this.timeout = initObj.timeout
      }
      else {
        this.timeout = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MopsActuators
    // Serialize message field [digital_outputs]
    bufferOffset = _serializer.uint8(obj.digital_outputs, buffer, bufferOffset);
    // Serialize message field [voltage0]
    bufferOffset = _serializer.float64(obj.voltage0, buffer, bufferOffset);
    // Serialize message field [voltage1]
    bufferOffset = _serializer.float64(obj.voltage1, buffer, bufferOffset);
    // Serialize message field [timeout]
    bufferOffset = _serializer.float64(obj.timeout, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MopsActuators
    let len;
    let data = new MopsActuators(null);
    // Deserialize message field [digital_outputs]
    data.digital_outputs = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [voltage0]
    data.voltage0 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [voltage1]
    data.voltage1 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [timeout]
    data.timeout = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 25;
  }

  static datatype() {
    // Returns string type for a message object
    return 'dcsc_fpga/MopsActuators';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '546bc7f707f4532234a4955136c8eadc';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    const resolved = new MopsActuators(null);
    if (msg.digital_outputs !== undefined) {
      resolved.digital_outputs = msg.digital_outputs;
    }
    else {
      resolved.digital_outputs = 0
    }

    if (msg.voltage0 !== undefined) {
      resolved.voltage0 = msg.voltage0;
    }
    else {
      resolved.voltage0 = 0.0
    }

    if (msg.voltage1 !== undefined) {
      resolved.voltage1 = msg.voltage1;
    }
    else {
      resolved.voltage1 = 0.0
    }

    if (msg.timeout !== undefined) {
      resolved.timeout = msg.timeout;
    }
    else {
      resolved.timeout = 0.0
    }

    return resolved;
    }
};

module.exports = MopsActuators;
