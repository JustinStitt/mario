
'''
Abstract classes to ensure implementation of
various Game-related functions such as Update 
and Render.
'''
class Updateable():
    def __init__(self, go=True, lifetime=-1):
        self.go = go
        self.frame = 0
        self.lifetime = lifetime # -1 is ad infinitum

    '''decorator to allow updates contingently (go)'''
    def _contingent_update(f):
        def wrapper(self):
            if not self.go: return
            if self.frame >= self.lifetime and self.lifetime != -1:
                self.handle_expiration()
                return
            f(self)
            self.frame += 1
        return wrapper

    @_contingent_update
    def update(self):
        raise NotImplementedError

    def handle_expiration(self):
        print(f'{self} has expired with {self.lifetime=}.', flush=True)
        self.go = False
        self.expired = True

class Renderable():
    def render(self):
        raise NotImplementedError
