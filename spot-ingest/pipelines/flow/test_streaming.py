from unittest import TestCase


class TestStreamPipeline(TestCase):
    def test_parse(self):
        from streaming import StreamPipeline
        old_line = '2022-09-03 07:10:39,1970,1,1,0,0,0,24.576,65.108.207.181,88.99.162.34,0,2816,ICMP,......,0,192,2,1152,0,0,0,0,0,0,0,0,0.0.0.0'
        old_fields = old_line.split(",")
        parsed_old = StreamPipeline.parse(old_fields)
        new_line = '2022-09-03 07:10:39,2022-09-03 07:11:04,24.576,65.108.207.181,88.99.162.34,0,2816,ICMP,......,0,192,2,1152,0,0,0,0,0,0,0,0,0,0,0.0.0.0,0.0.0.0,0,0,00:00:00:00:00:00,00:00:00:00:00:00,00:00:00:00:00:00,00:00:00:00:00:00,0-0-0,0-0-0,0-0-0,0-0-0,0-0-0,0-0-0,0-0-0,0-0-0,0-0-0,0-0-0,    0.000,    0.000,    0.000,0.0.0.0,0/0,1,1970-01-01 00:00:00.000'
        new_fields = new_line.split(",")
        parsed_new = StreamPipeline.parse(new_fields)

        assert len(parsed_old) == len(parsed_new)
        for i in range(len(parsed_new)):
            assert parsed_old[i] == parsed_new[i]


