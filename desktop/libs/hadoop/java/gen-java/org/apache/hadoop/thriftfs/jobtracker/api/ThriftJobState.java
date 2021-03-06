/**
 * Autogenerated by Thrift
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 */
package org.apache.hadoop.thriftfs.jobtracker.api;


import java.util.Map;
import java.util.HashMap;
import org.apache.thrift.TEnum;
/**
 * Enum version of the ints in JobStatus
 */
public enum ThriftJobState implements TEnum{
    RUNNING(1),
    SUCCEEDED(2),
    FAILED(3),
    PREP(4),
    KILLED(5);

  private static final Map<Integer, ThriftJobState> BY_VALUE = new HashMap<Integer,ThriftJobState>() {{
    for(ThriftJobState val : ThriftJobState.values()) {
      put(val.getValue(), val);
    }
  }};

  private final int value;

  private ThriftJobState(int value) {
    this.value = value;
  }

  /**
   * Get the integer value of this enum value, as defined in the Thrift IDL.
   */
  public int getValue() {
    return value;
  }

  /**
   * Find a the enum type by its integer value, as defined in the Thrift IDL.
   * @return null if the value is not found.
   */
  public static ThriftJobState findByValue(int value) { 
    return BY_VALUE.get(value);
  }
}
