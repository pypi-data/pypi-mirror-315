import unittest

import pygame

from mode import ModeTest


class TestModeBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.display.set_mode((1, 1), pygame.NOFRAME)

    def test_draw(self):
        # Arrange
        screen = pygame.Surface((6, 6))
        screen.fill(pygame.Color('white'))
        mode = ModeTest()
        # Act
        mode.draw(screen)
        # Assert
        for y in range(6):
            for x in range(6):
                expected = pygame.Color('white')
                if 0 < x < 5 and 0 < y < 5:
                    expected = pygame.Color('red')
                if x == 2 and y == 4:
                    expected = pygame.Color('black')
                if x == 3 and y == 2:
                    expected = pygame.Color('green')
                if x == 5 and y in {0, 5}:
                    expected = pygame.Color('blue')
                self.assertEqual(screen.get_at((x, y)), expected)

    def test_cleanup(self):
        # Arrange
        mode = ModeTest()
        # Act
        mode.cleanup()
        # Assert
        self.assertEqual(len(mode.sprites_all), 0)


if __name__ == '__main__':
    unittest.main()
