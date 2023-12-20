import operator
from collections import defaultdict
from functools import reduce

from toolbox.toolbox import input_file_name

button_presses_part_2 = 0
part_2_done = False


class Pulse:
    def __init__(self, source, destination, type):
        self.source = source
        self.destination = destination
        self.type = type

    def __repr__(self):
        return f'pulse: {self.source} -> {self.type} -> {self.destination}'


class Module:

    def __init__(self, name):
        self.name = name
        self.outgoing = []
        self.incoming = []
        self.pulses_sent = {'l': 0, 'h': 0}

    #
    # def on_receive_signal(self, p: Pulse):
    #     print(f'sent: {p.source} -> {p.type} -> {self.name}')

    def connect_to(self, other):
        print(f'{self.name} connecting to {other.name}')
        self.outgoing.append(other)
        other.incoming.append(self)


class Sink(Module):

    def __init__(self, name):
        super().__init__(name)

    def on_receive_signal(self, p: Pulse):
        self.pulses_sent[p.type] += 1
        # super().on_receive_signal(p)
        # print(f'doing nothing, {self.name} is a sink...')

    def connect_to(self, other):
        # print(f'{self.name} connecting to {other.name}')
        self.outgoing.append(other)
        other.incoming.append(self)


class Broadcaster(Module):

    def __init__(self, name):
        super().__init__(name)

    def on_receive_signal(self, p: Pulse):
        # super().on_receive_signal(p)
        self.pulses_sent[p.type] += len(self.outgoing)
        return [Pulse(self.name, c.name, p.type) for c in self.outgoing]


class FlipFlop(Module):

    def __init__(self, name):
        super().__init__(name)
        self.on = False

    def on_receive_signal(self, p: Pulse):
        # super().on_receive_signal(p)

        if p.type == 'h':
            return []

        self.on = not self.on
        outgoing_pulse_type = 'h' if self.on else 'l'
        self.pulses_sent[outgoing_pulse_type] += len(self.outgoing)
        return [Pulse(self.name, c.name, outgoing_pulse_type) for c in self.outgoing]


def constant_factory(value):
    return lambda: value


class ConjunctionModule(Module):

    def __init__(self, name):
        super().__init__(name)
        self.last_received_per_incoming = defaultdict(constant_factory('l'))
        self.part_2_hack = defaultdict(int)

    def on_receive_signal(self, p: Pulse):
        # super().on_receive_signal(p)
        self.last_received_per_incoming[p.source] = p.type

        if self.name == 'zh' and p.type == 'h':
            print(f'zh received h from {p.source} after {button_presses_part_2} presses')
            self.part_2_hack[p.source] = button_presses_part_2
            global part_2_done
            part_2_done |= reduce(lambda a, b: a and b, [self.part_2_hack[x.name] > 0 for x in self.incoming], True)

        num_high = 0
        for x in self.incoming:
            if self.last_received_per_incoming[x.name] == 'h':
                num_high += 1

        outgoing_pulse_type = 'l' if num_high == len(self.incoming) else 'h'
        self.pulses_sent[outgoing_pulse_type] += len(self.outgoing)

        return [Pulse(self.name, c.name, outgoing_pulse_type) for c in self.outgoing]


class Button(Module):

    def __init__(self, name):
        super().__init__(name)

    def on_receive_signal(self, p: Pulse):
        return [Pulse(self.name, c.name, p.type) for c in self.outgoing]


def part_1(problem):
    modules = []
    targets = []

    for line in problem:
        m, t = line.split(' -> ')
        if m == "broadcaster":
            modules.append(Broadcaster('broadcaster'))
        elif '%' in m:
            modules.append(FlipFlop(m[1:]))
        elif '&' in m:
            modules.append(ConjunctionModule(m[1:]))
        else:
            print(">>>>>>> OH NO")
        targets.append(t.strip())

    module_index = {m.name: m for m in modules}

    for m, t in zip(modules, targets):
        sliced = t.split(',')
        for s in sliced:
            k = s.strip()
            if k not in module_index.keys():
                module_index[k] = Sink(k)
            m.connect_to(module_index[s.strip()])

    button = Button('button')
    button.connect_to(module_index['broadcaster'])

    button_presses = 1000

    for _ in range(button_presses):
        event_bus = [Pulse('button', 'broadcaster', 'l')]
        while event_bus:
            pulse = event_bus.pop(0)
            new_pulses = module_index[pulse.destination].on_receive_signal(pulse)
            if new_pulses:
                event_bus += new_pulses

    low_sent = sum((x.pulses_sent['l'] for x in modules)) + button_presses
    high_sent = sum((x.pulses_sent['h'] for x in modules))

    return low_sent * high_sent


def part_2(problem):
    modules = []
    targets = []

    for line in problem:
        m, t = line.split(' -> ')
        if m == "broadcaster":
            modules.append(Broadcaster('broadcaster'))
        elif '%' in m:
            modules.append(FlipFlop(m[1:]))
        elif '&' in m:
            modules.append(ConjunctionModule(m[1:]))
        else:
            print(">>>>>>> OH NO")
        targets.append(t.strip())

    module_index = {m.name: m for m in modules}

    for m, t in zip(modules, targets):
        sliced = t.split(',')
        for s in sliced:
            k = s.strip()
            if k not in module_index.keys():
                module_index[k] = Sink(k)
            m.connect_to(module_index[s.strip()])

    button = Button('button')
    button.connect_to(module_index['broadcaster'])

    global button_presses_part_2
    global part_2_done

    while not part_2_done:
        event_bus = [Pulse('button', 'broadcaster', 'l')]
        while event_bus:
            pulse = event_bus.pop(0)
            new_pulses = module_index[pulse.destination].on_receive_signal(pulse)
            if new_pulses:
                event_bus += new_pulses
        button_presses_part_2 += 1

    print('yay')
    hack = module_index['zh'].part_2_hack
    return reduce(operator.mul, [x + 1 for x in hack.values()], 1)


if __name__ == '__main__':
    with open(input_file_name) as problem:
        print(part_1(problem))
    with open(input_file_name) as problem:
        print(part_2(problem))
