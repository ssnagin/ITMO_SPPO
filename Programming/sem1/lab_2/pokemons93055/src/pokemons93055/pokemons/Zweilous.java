package pokemons93055.pokemons;

import ru.ifmo.se.pokemon.Type;
import pokemons93055.move.physical.DoubleHit;


/**
 * Defines a new Pokemon - Zweilous.
 *
 * @author ssngn
 */
public class Zweilous extends Deino {

    private final double HP = 254;
    private final double ATTACK = 157;
    private final double DEFENCE = 130;
    private final double SPECIAL_ATTACK = 121;
    private final double SPECIAL_DEFENCE = 130;
    private final double SPEED = 108;

    /**
     *
     * @param name - Name of Zweilous
     * @param level - initial level of pokemon
     */
    public Zweilous(String name, int level) {
        super(name, level);

        setType(Type.DARK, Type.DRAGON);
        setStats(HP, ATTACK, DEFENCE, SPECIAL_ATTACK, SPECIAL_DEFENCE, SPEED);

        addMove(new DoubleHit());
    }
}
