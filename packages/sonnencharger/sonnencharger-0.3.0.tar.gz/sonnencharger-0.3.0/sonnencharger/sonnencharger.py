import asyncio
import logging
import traceback

import pymodbus.client as ModbusClient

from pymodbus import (
    FramerType,
    ModbusException,
    pymodbus_apply_logging_config,
)

LOGGER = logging.getLogger(__package__)

ADDR_SC_SERIALNO        = 990
ADDR_SC_MODEL           = 1000
ADDR_SC_HWREV           = 1010
ADDR_SC_SWREV           = 1015
ADDR_SC_NUMCONN         = 1020

ADDR_CONN_STATE         = 0

ADDR_CONN_VHCL_PHS      = 1
ADDR_CONN_VHCL_MAX_CURR = 2
ADDR_CONN_VHCL_TGT_CURR = 4
ADDR_CONN_VHCL_MAX_PWR  = 44
ADDR_CONN_VHCL_REQ_NRGY = 46

ADDR_CONN_NET_FREQUENCY = 6

ADDR_CONN_L1_VOLTAGE    = 8
ADDR_CONN_L2_VOLTAGE    = 10
ADDR_CONN_L3_VOLTAGE    = 12

ADDR_CONN_L1_CURRNT     = 14
ADDR_CONN_L2_CURRNT     = 16
ADDR_CONN_L3_CURRNT     = 18

ADDR_CONN_L1_ACT_PWR    = 20
ADDR_CONN_L2_ACT_PWR    = 22
ADDR_CONN_L3_ACT_PWR    = 24

ADDR_CONN_TOT_ACT_PWR   = 26
ADDR_CONN_PWR_FACTOR    = 28

ADDR_CONN_SESS_NRGY_IMP = 30
ADDR_CONN_SESS_DURATION = 32
ADDR_CONN_SESS_DEPART   = 36
ADDR_CONN_SESS_ID       = 40

ADDR_CONN_TYPE          = 1022
ADDR_CONN_NUM_PHS       = 1023
ADDR_CONN_MAX_CURR      = 1028

class sonnencharger:
  def __init__(self, ipaddress, port=502) -> None:
    pymodbus_apply_logging_config("ERROR")
    self._sc_host = ipaddress
    self._sc_port = port
    self.system_data = {}

  async def _decode_string(self, offset, length):
    try:
      rsp = await self._sc_conn.read_input_registers(address=offset, count=length)
      return self._sc_conn.convert_from_registers(rsp.registers, self._sc_conn.DATATYPE.STRING).rstrip('\x00')
    except ModbusException as exc:
      e = traceback.format_exc()
      LOGGER.error(f"Unable to read charger value. [{exc}]\n{e}")
      return ""

  async def _decode_uint8(self, offset):
    try:
      rsp = await self._sc_conn.read_input_registers(address=offset, count=1)
      return self._sc_conn.convert_from_registers(rsp.registers, self._sc_conn.DATATYPE.UINT16)
    except ModbusException as exc:
      e = traceback.format_exc()
      LOGGER.error(f"Unable to read charger value. [{exc}]\n{e}")
      return False

  async def _decode_uint16(self, offset):
    try:
      rsp = await self._sc_conn.read_input_registers(address=offset, count=2)
      return self._sc_conn.convert_from_registers(rsp.registers, self._sc_conn.DATATYPE.UINT32)
    except ModbusException as exc:
      e = traceback.format_exc()
      LOGGER.error(f"Unable to read charger value. [{exc}]\n{e}")
      return False

  async def _decode_uint64(self, offset):
    try:
      rsp = await self._sc_conn.read_input_registers(address=offset, count=4)
      return self._sc_conn.convert_from_registers(rsp.registers, self._sc_conn.DATATYPE.UINT64)
    except ModbusException as exc:
      e = traceback.format_exc()
      LOGGER.error(f"Unable to read charger value. [{exc}]\n{e}")
      return False

  async def _decode_float32(self, offset):
    try:
      rsp = await self._sc_conn.read_input_registers(address=offset, count=2)
      return self._sc_conn.convert_from_registers(rsp.registers, self._sc_conn.DATATYPE.FLOAT32)
    except ModbusException as exc:
      e = traceback.format_exc()
      LOGGER.error(f"Unable to read charger value. [{exc}]\n{e}")
      return False

  async def _collect_sysinfo(self):
    self._sc_conn = ModbusClient.AsyncModbusTcpClient(
      host=self._sc_host,
      port=self._sc_port,
      framer=FramerType.SOCKET,
    )
    await self._sc_conn.connect()
    # Serial Number
    serial = await self._decode_string(ADDR_SC_SERIALNO, 10)
    self.system_data['serial'] = serial

    # Model
    model = await self._decode_string(ADDR_SC_MODEL, 10)
    self.system_data['model'] = model

    # HW version
    hwrev = await self._decode_string(ADDR_SC_HWREV, 5)
    self.system_data['hwrevision'] = hwrev

    # SW version
    swrev = await self._decode_string(ADDR_SC_SWREV, 5)
    self.system_data['swrevision'] = swrev

    # no# of connectors
    conns = await self._decode_uint8(ADDR_SC_NUMCONN)
    self.system_data['connectors'] = conns

    self._sc_conn.close()

  async def _collect_connector_info(self):
    self._sc_conn = ModbusClient.AsyncModbusTcpClient(
      host=self._sc_host,
      port=self._sc_port,
      framer=FramerType.SOCKET,
    )
    await self._sc_conn.connect()
    self.connector_data = {}
    for c in range(self.system_data['connectors']):
      offset = c * 100
      connector = {}
      # connector state
      conn_state = await self._decode_uint8(ADDR_CONN_STATE)
      connector['state_numeric'] = conn_state

      if conn_state == 1:
        connector['state'] = "Available"
      elif conn_state == 2:
        connector['state'] = "No cable connected"
      elif conn_state == 3:
        connector['state'] = "Waiting for vehicle to reespond"
      elif conn_state == 4:
        connector['state'] = "Charging"
      elif conn_state == 5:
        connector['state'] = "Vehicle has paused charging"
      elif conn_state == 6:
        connector['state'] = "EVSA has paused charging"
      elif conn_state == 7:
        connector['state'] = "Charging has ended"
      elif conn_state == 8:
        connector['state'] = "Charging fault"
      elif conn_state == 9:
        connector['state'] = "Unpausing charging"
      elif conn_state == 10:
        connector['state'] = "Unavailable"
      else:
        connector['state'] = "Unknown state!"

      # Vehicle connected phase
      conn_phs = await self._decode_uint8(ADDR_CONN_VHCL_PHS)
      connector['vehicle_connected_phases_code'] = conn_phs

      if conn_phs == 0:
        connector['vehicle_connected_phases'] = "Three phases"
        connector['vehicle_connected_phases_numeric'] = 3
      elif conn_phs == 1:
        connector['vehicle_connected_phases'] = "Single phase (L1)"
        connector['vehicle_connected_phases_numeric'] = 1
      elif conn_phs == 2:
        connector['vehicle_connected_phases'] = "Single phase (L2)"
        connector['vehicle_connected_phases_numeric'] = 1
      elif conn_phs == 3:
        connector['vehicle_connected_phases'] = "Single phase (L3)"
        connector['vehicle_connected_phases_numeric'] = 1
      elif conn_phs == 4:
        connector['vehicle_connected_phases'] = "Unknown number of phases"
        connector['vehicle_connected_phases_numeric'] = -1
      elif conn_phs == 5:
        connector['vehicle_connected_phases'] = "Two phases"
        connector['vehicle_connected_phases_numeric'] = 2
      else:
        connector['vehicle_connected_phases'] = "Unknown number of phases"
        connector['vehicle_connected_phases_numeric'] = -1

      # ev max phase current (limited to 3 digits)
      connector['ev_max_phase_current'] = round(await self._decode_float32(ADDR_CONN_VHCL_MAX_CURR), 3)

      # target current (limited to 3 digits)
      connector['target_current'] = round(await self._decode_float32(ADDR_CONN_VHCL_TGT_CURR), 3)

      # net frequency
      connector['net_frequency'] = round(await self._decode_float32(ADDR_CONN_NET_FREQUENCY), 3)

      # l1 L-N voltage
      connector['l1_ln_voltage'] = round(await self._decode_float32(ADDR_CONN_L1_VOLTAGE), 3)

      # l2 L-N voltage
      connector['l2_ln_voltage'] = round(await self._decode_float32(ADDR_CONN_L2_VOLTAGE), 3)

      # l3 L-N voltage
      connector['l3_ln_voltage'] = round(await self._decode_float32(ADDR_CONN_L3_VOLTAGE), 3)

      # l1 current
      connector['l1_current'] = round(await self._decode_float32(ADDR_CONN_L1_CURRNT), 3)

      # l2 current
      connector['l2_current'] = round(await self._decode_float32(ADDR_CONN_L2_CURRNT), 3)

      # l3 current
      connector['l3_current'] = round(await self._decode_float32(ADDR_CONN_L3_CURRNT), 3)

      # l1 active power
      connector['l1_active_power'] = round(await self._decode_float32(ADDR_CONN_L1_ACT_PWR), 3)

      # l2 active power
      connector['l2_active_power'] = round(await self._decode_float32(ADDR_CONN_L2_ACT_PWR), 3)

      # l2 active power
      connector['l3_active_power'] = round(await self._decode_float32(ADDR_CONN_L3_ACT_PWR), 3)

      # total active power
      connector['total_active_power'] = round(await self._decode_float32(ADDR_CONN_TOT_ACT_PWR), 3)

      # power factor
      connector['power_factor'] = round(await self._decode_float32(ADDR_CONN_PWR_FACTOR), 3)

      # impoerted energy in running session (kWh)
      connector['active_session_imported_energy'] = round(await self._decode_float32(ADDR_CONN_SESS_NRGY_IMP), 3)

      # session duration (s)
      connector['active_session_duration'] = await self._decode_uint64(ADDR_CONN_SESS_DURATION)

      # session departure timee (s)
      connector['session_departure_time'] = await self._decode_uint64(ADDR_CONN_SESS_DEPART)

      # running session id
      connector['session_id'] = await self._decode_uint64(ADDR_CONN_SESS_ID)

      # ev max power
      connector['ev_max_power'] = round(await self._decode_float32(ADDR_CONN_VHCL_MAX_PWR), 3)

      # ev max power
      connector['ev_required_energy'] = round(await self._decode_float32(ADDR_CONN_VHCL_REQ_NRGY), 3)

      # connector type
      conn_type = await self._decode_uint8(ADDR_CONN_TYPE + offset)
      connector['type_numeric'] = conn_type
      if conn_type == 1:
        connector['type'] = "Socket Type 2"
      elif conn_type == 2:
        connector['type'] = "CableType2"
      else:
        connector['type'] = "Unknown connector type"

      # noumber of phases
      connector['num_phases'] = await self._decode_uint8(ADDR_CONN_NUM_PHS + offset)

      # pase 1 connected
      for p in range(1,4):
        connector['l{}_phase'.format(p)] = await self._decode_uint16(ADDR_CONN_NUM_PHS + p + offset)

      # max current
      connector['max_current'] = await self._decode_float32(ADDR_CONN_MAX_CURR + offset)

      self.connector_data[c] = connector
      self._sc_conn.close()

  # General system info
  def get_sysinfo(self):
    asyncio.run(
      self._collect_sysinfo()
    )
    return self.system_data

  def get_connectors(self):
    asyncio.run(
      self._collect_connector_info()
    )
    return self.connector_data
