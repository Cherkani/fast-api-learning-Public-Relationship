def solution(laps):
    best_times = {}
    elimination_order = []
    eliminated_drivers = set()  # Track drivers eliminated in previous laps

    for lap in laps:
        # Update best times for active drivers
        for entry in lap:
            name, time_str = entry.split()
            if name in eliminated_drivers:
                continue  # Skip eliminated drivers
            time = int(time_str)
            if name not in best_times or time < best_times[name]:
                best_times[name] = time

        # Find the slowest best time(s) among active drivers
        if not best_times:
            break  # All drivers eliminated
        max_time = max(best_times.values())
        eliminated = [name for name, t in best_times.items() if t == max_time]

        # Sort alphabetically and add to elimination order
        eliminated.sort()
        elimination_order.extend(eliminated)

        # Mark these drivers as eliminated and remove from active tracking
        eliminated_drivers.update(eliminated)
        for name in eliminated:
            del best_times[name]

    return elimination_order

# Example usage:
laps = [
    ["Harold 154", "Gina 155", "Juan 160"],
    ["Harold 151", "Gina 153", "Juan 152"],
    ["Harold 148", "Gina 150", "Juan 149"]
]
print(solution(laps))  # Output: ["Juan", "Gina", "Harold"]