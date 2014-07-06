from CStructures import GAME_CAMERA
from PlayerState import PlayerState


# pointer to GAME_CAMERA structure
CAMERA_PTR = 0x0082F890
# pointers to players' PLAYER structures
P1_PTR = 0x008320A0
P2_PTR = P1_PTR + 4
# pointers to players' PLAYER_TEAM structures
P1_TEAM_PTR = 0x00831DF4
P2_TEAM_PTR = 0x00831EF8
# pointers to players' HITBOX_SET structures
P1_HBS = 0x007EAC08
P2_HBS = 0x007EAC44


class GameState:
	def __init__(self, environment):
		self.env = environment
		self.process = self.env.process
		self.p1 = PlayerState(self.env, 1, P1_PTR, P1_TEAM_PTR, P1_HBS)
		self.p2 = PlayerState(self.env, 2, P2_PTR, P2_TEAM_PTR, P2_HBS)
		self.camera = GAME_CAMERA()
	

	def update(self):
		self.process._RPM(CAMERA_PTR, self.camera)

		self.p1.update()
		self.p2.update()
