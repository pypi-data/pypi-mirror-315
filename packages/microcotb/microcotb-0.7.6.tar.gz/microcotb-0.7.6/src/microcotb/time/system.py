'''
Created on Nov 23, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''
from microcotb.time.value import TimeValue, TimeConverter
from microcotb.clock import Clock
import time

class SystemTimeout(Exception):
    pass

class SystemTime:
    ResetTime = None
    ForceSleepOnAdvance = None
    _global_time = TimeValue(0, TimeValue.BaseUnits)
    _min_sleep_time = TimeValue(
                        TimeConverter.rescale(200, 'us', TimeValue.BaseUnits), 
                        TimeValue.BaseUnits)
    _timeout_setting = None
    
    @classmethod 
    def reset(cls):
        if cls.ResetTime is None:
            cls._global_time = TimeValue(0, TimeValue.BaseUnits)
        else:
            cls._global_time = cls.ResetTime.clone()
        
    @classmethod 
    def current(cls) -> TimeValue:
        return cls._global_time
    
    @classmethod 
    def set_timeout(cls, delta_time:TimeValue):
        cls._timeout_setting = cls.current() + delta_time
        
    @classmethod 
    def clear_timeout(cls):
        cls._timeout_setting = None
        
        
    @classmethod 
    def set_units(cls, units:str):
        cls._global_time = TimeValue(cls._global_time.time, units)
        
    @classmethod 
    def advance(cls, time_or_timevalue, units:str=None):
        if isinstance(time_or_timevalue, TimeValue):
            tstep = time_or_timevalue
        elif isinstance(time_or_timevalue, int) and units is not None:
            tstep = TimeValue(time_or_timevalue, units)
        else:
            raise ValueError
        
        cls._global_time += tstep
        #if cls._min_sleep_time < tstep:
        #    time.sleep_us(int(tstep.time_in('us')))
            
        if cls._timeout_setting is not None:
            if cls._global_time >= cls._timeout_setting:
                raise SystemTimeout(f'Timeout at {cls.current()}')
        
        for clk in Clock.all():
            clk.time_is_now(cls._global_time)
            if cls.ForceSleepOnAdvance:
                time.sleep(cls.ForceSleepOnAdvance)
            