from elections.services.results_engine import ResultsEngine


class SeatAllocator:
    """
    Gère la répartition des sièges
    """

    @staticmethod
    def allocate_seats(total_seats):

        results = ResultsEngine.get_global_results()

        total_votes = sum(results.values())

        if total_votes == 0:
            return {}

        # 🔥 majorité absolue
        for party, votes in results.items():
            if votes / total_votes > 0.5:
                return {party: total_seats}

        # ❌ pas de majorité
        sorted_lists = sorted(results.items(), key=lambda x: x[1], reverse=True)

        seats = {}

        # 🥇 prime majoritaire
        first_party = sorted_lists[0][0]
        majority_bonus = total_seats // 2
        seats[first_party] = majority_bonus

        remaining_seats = total_seats - majority_bonus

        # 🚫 seuil 5%
        eligible = {
            party: votes
            for party, votes in results.items()
            if (votes / total_votes) >= 0.05
        }

        total_eligible_votes = sum(eligible.values())

        if remaining_seats == 0:
            return seats

        quotient = total_eligible_votes / remaining_seats

        remainders = {}

        # attribution initiale
        for party, votes in eligible.items():
            seat_count = int(votes // quotient)
            seats[party] = seats.get(party, 0) + seat_count

            remainders[party] = votes % quotient

        # distribution des restes
        assigned = sum(seats.values())
        seats_left = total_seats - assigned

        sorted_remainders = sorted(remainders.items(), key=lambda x: x[1], reverse=True)

        for i in range(seats_left):
            party = sorted_remainders[i][0]
            seats[party] += 1

        return seats