class Clock:
    cycle_count = 0



    @classmethod
    def posEdgeClk(cls):
        cls.cycle_count += 1