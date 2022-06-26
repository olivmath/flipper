# @version ^0.3.0

flip: public(bool)

event Fliped:
  state: bool

@external
def flipping() -> bool:
  self.flip = not self.flip
  log Fliped(self.flip)
  return self.flip

@external
def __init__():
  self.flip = True
