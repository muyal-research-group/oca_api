class Utils:
    @staticmethod
    def check_string(x:str,low:int = 8, high:int = 32):
        s_len = len(x)
        return x.isalnum() and (s_len >=low and s_len <=high)