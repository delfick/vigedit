class VIG_Options(object):
    def __init__(self):
        """
            TraceLevel determines what gets printed
            
             0 = nothing
             1 = only error messages
             2 = error and warning messages
             3 = error, warning and level 1 info
             4 = error, warning, level1 and level 2 info
             
             -1 = only level 1 info
             -2 = only level 2 info
             -3 = only level 1 and 2 info
        """
        self.TraceLevel = 3

        """
            TraceKeys determines whether or not to print captured keys
        """
        self.TraceKeys = False

opts = VIG_Options()
