from alohomora import Alohomora


class TestAlohomora:

    def test_lookup(self):
        spell = Alohomora('prod', 'birdie', mock=True)
        spell.render('test/files/birdie.j2')
