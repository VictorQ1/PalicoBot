# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from fuzzywuzzy import process


class ActionMonsterInfo(Action):

    def name(self) -> Text:
        return "action_monster_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        monster_data = {
            "Rathalos": {
                "weakness": "Dragon/Thunder",
                "resistant": "Fire",
                "habitat": "Ancient Forest",
                "strategy": "Ensure you have adequate Fire Resistance and a generous supply of Antidotes, or Poison Resistance. Rathalos utilizes his talons for poisoning attacks. \nRathalos is an agile flier, but his airborne assaults can be grounded with Flash Pods. Exploit this vulnerability by bringing him down, focusing on head attacks, and repeating the process. Attacking his tail mid-flight is also effective, and severing it compels him to land",
            },
            "Acidic Glavenus": {
                "weakness": "Fire",
                "resistant": "Water/Ice",
                "habitat": "Rotten Vale",
                "strategy": "Prepare for the onslaught of classic Glavenus maneuvers when Acidic Glavenus enters its acidic state. Expect double tail slams, sweeping 360-degree area assaults, and powerful bites. Positioning yourself wisely and predicting its movements will be crucial in this phase. To maximize your safety, stay behind Acidic Glavenus during the battle. Given that most of its attacks are front-facing, positioning yourself strategically behind the creature provides a safer vantage point. As Acidic Glavenus transitions into its crystalized state, it undergoes a remarkable transformation, becoming more agile and dynamic.",
            },
            "Ancient Leshen": {
                "weakness": "Fire",
                "resistant": "Water",
                "habitat": "Ancient Forest",
                "strategy": "Strategic planning and collaboration within a well-coordinated team are imperative. The quest is specifically designed for a 4-player group, emphasizing the importance of organizing roles for each member to ensure a streamlined and effective approach to the encounter. Equipping both Temporal Mantles and Health Boosters adds an extra layer of defense and sustenance, increasing your team's chances of success. Considering a Health Augment on your weapon proves effective in countering the chip damage inflicted by the Leshen's crow aura, providing a valuable means of self-sustainability. \nIt's highly recommended to have at least one player dedicated to healing the team, significantly improving the overall success rate. When the Ancient Leshen summons his Jagras pack make sure to eliminate them as quick as possible. These Jagras are tanky and are highly annoying due to the vast number of them while the Leshen will enclose players in a root prison while distracted. Players that have long weapons like a longsword should focus them down to allow the other teammates to focus on the Ancient Leshen. If overrun use flash pods to temporarily stun the Leshen and all the Jagras. ",
            },
            "Anjanath": {
                "weakness": "Water/Thunder/Ice",
                "resistant": "Fire/Dragon",
                "habitat": "Ancient Forest",
                "strategy": "Opt for a weapon that exploits Anjanath's elemental weaknesses, which include Water, Thunder, and Ice. Initiate the fight by attempting to mount Anjanath. Jump off ledges and use the main attack to trigger the mount, focusing on weak spots. Successfully mounting Anjanath not only deals damage but also creates advantageous knockdown opportunities. After knocking Anjanath down, target its tail for severance. Strategic positioning is crucial for minimizing damage from Anjanath's devastating frontal attacks. Stay between its legs to mitigate the threat from its powerful mouth, ensuring a safer engagement. When Anjanath enters its berserk state with fire attacks, indicated by sprouting fins, closely observe its movements. Dodge the fire attacks, especially impactful ones, to avoid significant damage.",
            },
            "Azure Rathalos": {
                "weakness": "Dragon/Ice",
                "resistant": "Fire",
                "habitat": "Ancient Forest/Elder's Recess",
                "strategy": "Azure Rathalos is a formidable foe, boasting a variety of aerial and ground-based attacks. To counter its aerial assaults, equip Flash Pods to ground it, creating opportunities for damage. Observe its flight patterns and find the right moment to knock it out of the sky. Once grounded, it loses the ability to perform consecutive attacks, making the fight much easier. Focus on its head and tail, aiming to sever the latter for additional rewards. When Azure Rathalos enters its enraged state, indicated by glowing eyes and a fiery aura, exercise caution. Avoid its powerful fire attacks and focus on evasion to minimize damage. Utilize the environment to your advantage, using ledges and slopes to mount Azure Rathalos and create additional damage opportunities.",
            },
            "Banbaro": {
                "weakness": "Dragon/Fire",
                "resistant": "Ice/Water",
                "habitat": "Hoarfrost Reach",
                "strategy": "Banbaro is a strong opponent in the frosty terrain. Prepare for the battle by ensuring your armor provides solid defense against physical attacks and icy assaults. Use fire or dragon weapons to maximize damage and take advantage of Banbaro's weaknesses. Use the clutch claw strategically when attacking from the side, and be ready to mount Banbaro when the chance arises, capitalizing on its vulnerability. \nBanbaro, being an ice-type creature, tends to inflict ice blight with its attacks. Arm yourself with Nulberries to quickly shake off this chilling effect. Additionally, consider weapons or items that bring the sting of poison, sleep, paralysis, or, particularly effective against Banbaro, stun. \nDuring the battle, focus on Banbaro's head and aim to break its formidable horns, hindering its devastating environmental attacks. Watch for its patterns, especially the ice boulders and tree-slamming maneuvers, and adapt your movements accordingly. When Banbaro is dazed or weakened, seize the opportunity to set traps or deploy bomb barrels. ",
            },
            "Barioth": {
                "weakness": "Fire/Thunder",
                "resistant": "Ice/Water",
                "habitat": "Hoarfrost Reach",
                "strategy": "Focus your attacks on Barioth's head for raw damage. If you're using elemental damage, target its claws for maximum effectiveness. The head takes the most damage overall, making it the prime target for both raw and elemental damage. Breaking Barioth's parts significantly weakens its attacks and makes the fight more manageable. Aim to break its face, arms, back, and tail. Breaking these parts alters Barioth's moveset, giving you openings to exploit. \nLearn to utilize the flinch shot mechanic to your advantage. Use the clutch claw to grab Barioth's head, soften its parts, and then perform a flinch shot into a wall. This can create additional openings for attacks and give you a significant advantage in the fight. \nLearn Barioth's attack patterns and practice effective dodging. Rolling into Barioth during its hip check attack grants you invincibility frames. When it jumps, running towards it can often help you avoid its aerial attacks.",
            },
            "Barroth": {
                "weakness": "Water(mud)/Fire(no mud)",
                "resistant": "Thunder",
                "habitat": "Wildspire Waste",
                "strategy": "Equip a weapon with water elemental damage to exploit Barroth's vulnerability. If using a melee weapon, focus on attacking weak spots revealed as the armor breaks off. Alternatively, choose a ranged weapon like a bow or bowgun for safer attacks. Opt for a ranged weapon with armor-piercing or explosive rounds to deal with Barroth's tough exterior. Stock up on healing items to withstand Barroth's powerful blows. Ensure your weapons and armor are upgraded for maximum effectiveness in the fight against Barroth. \nBarroth's mud armor provides additional protection, making it more resistant to damage. Use water-based attacks to soften the mud armor and expose Barroth's weak points. Focus on breaking Barroth's head, arms, and tail to weaken its attacks and create openings for damage. When Barroth charges, dodge to the side to avoid its powerful attacks. Use the environment to your advantage, utilizing slopes and ledges to mount Barroth and create additional damage opportunities.",
            },
            "Bazelgeuse": {
                "weakness": "Thunder/Dragon/Ice",
                "resistant": "Fire",
                "habitat": "Ancient Forest/Wildspire Waste/Elder's Recess",
                "strategy": "Equip high-defense armor with fire resistance. Choose a weapon that suits your comfort level, considering both melee and ranged options. Ranged weapons like the Bow or Bowgun provide safety at a distance. Utilize weapons with Thunder damage for increased effectiveness, and exploit poison, sleep, or paralysis to gain an advantage during the battle. \nThe scales that Bazelgeuse scatters explode with tremendous force, making them extremely deadly. Focus on its legs to knock it down, and then knock out its scale-generating organs under its chin and tail. (Severing the tail reduces the amount of bombs released at once, but the tail stump still keeps a few after the tail is severed.) \nEnsure you bring healing items such as Mega Potions and Max Potions, along with traps, Flash Pods, Barrel Bombs, and other utility items.",
            },
            "Behemoth": {
                "weakness": "Dragon",
                "resistant": "Thunder/Fire",
                "habitat": "Elder's Recess",
                "strategy": "Cooperation is a must. A Tank or Evasion Tank is absolutely essential to the run. Lance, IG and shield users should tank the monster: Let the tank start to get aggro first. Do not engage until the tank has enmity confirmed by the combat text. Bring healing items to help your teammates such as Lifepowder. 3 on hand and 10 combination reserves will ensure everyone stays alive. \nThe boss summons COMETS. Your team should drop them in accessible areas of the arena. When the large meteor AOE comes, put the COMET between you and the middle of the arena where the large meteor will land. The floor turns red and the boss glows red as a signal. When Charybdis is cast, a player will be selected with a gust of wind similar to the starting of a Kushala Tornado. Move closer to a wall if possible to ensure that the team isn't affected during combat. \nIt is worth noting that if everyone leaves the zone he is currently in he will begin to regenerate health.",
            },
            "Beotodus": {
                "weakness": "Fire/Thunder",
                "resistant": "Ice/Dragon",
                "habitat": "Hoarfrost Reach",
                "strategy": "Equip a weapon with fire or thunder elemental damage to exploit Beotodus' weakness. Focus on attacking its head and tail for maximum damage. Breaking Beotodus' parts weakens its attacks and creates openings for additional damage. Aim to break its head, arms, and tail during the fight. Use the clutch claw to soften Beotodus' parts and create additional damage opportunities. \nBeotodus' icy breath attack can inflict ice blight, slowing your movement speed. Use Nulberries to remove ice blight and maintain mobility during the fight. Be prepared to dodge Beotodus' charging attacks and icy projectiles. Position yourself strategically to avoid its attacks and create openings for counterattacks. Utilize the environment to your advantage, using slopes and ledges to mount Beotodus and deal additional damage.",
            },
            "Brachydios": {
                "weakness": "Water/Ice",
                "resistant": "Fire",
                "habitat": "Elder's Recess",
                "strategy": "Equip a weapon with water or ice elemental damage to exploit Brachydios' weakness. Hitting Brachydios' hands with Water or Ice damage will wash off the slime, preventing explosions and slime from that hand, until Brachydios reapplies the slime with its mouth. \nBrachydios' hands can also be broken, permanently preventing it from coating the respective hand with slime. Its head can also be broken, however, it takes tremendeous damage for it to break. \nBlast Resistance will help prevent Blastscourge. Full immunity is advised",
            },
            "Brute Tigrex": {
                "weakness": "Water/Thunder",
                "resistant": "Fire/Ice",
                "habitat": "Guiding Lands",
                "strategy": "Ensure that your armor is either high-rank or master-rank with strong defense against physical and dragon damage. Focus on sets that offer high ice resistance, given Brute Tigrex's ice attacks. Additionally, consider wielding a thunder-element weapon to exploit its weakness and deal increased damage. \nBrute Tigrex introduces new attack combinations, such as a paw slam and arm sweep. Stay alert and ready to evade these maneuvers. Frequent roars are part of its arsenal, and it's advisable to bring Earplugs to mitigate their disruptive effects. The sonic beam attack has an unexpectedly broad range, so learning visual cues is essential for effective dodging. \nCustomize your armor skills to suit your playstyle. Skills like Health Boost, Evade Window, and Thunder Attack can significantly enhance your performance. If possible, consider using augments to add defensive or offensive enhancements to your weapon for added flexibility.",
            },
            "Coral Pukei-Pukei": {
                "weakness": "Ice/Thunder",
                "resistant": "Water",
                "habitat": "Coral Highlands",
                "strategy": "Watch out for its strong water attacks from the mouth and tail, causing big damage and waterblight. After munching on a giant mushroom, it deals even more damage with water elemental attacks. Equip water-resistant armor to mitigate damage from the Coral Pukei-Pukei's water attacks. This helps you stay in the fight longer. \nUse weapons with ice or thunder elemental damage to exploit the Coral Pukei-Pukei's weaknesses.",
            },
            "Deviljho": {
                "weakness": "Dragon/Thunder",
                "resistant": "Nothing",
                "habitat": "entire map",
                "strategy": "Hunters should attack its weakpoints in the Head and Chest. The tail can be severed but is not a weakpoint. \nCan inflict Defense Down debuff with the monsters it uses as bludgeons, or by picking up the hunter with its mouth. For monsters too big to pick up, he will occasionally "
                "take a bite,"
                " out of them, dealing a decent amount of damage (seems to be 500, even in solo). For these reasons, he can serve as a valuable "
                "ally,"
                " for a hunter, so long as they steer clear of it.",
            },
            "Diablos": {
                "weakness": "Ice/Dragon/Water",
                "resistant": "Fire",
                "habitat": "Wildspire Waste",
                "strategy": "Ice is the most effective element against it. Diablos can be forcefully brought to the surface by using loud sounds, such as with a screamer pod, Noios and the Hunting Horn melody Sonic Waves. Its charging attack, while devastatingly powerful, can be baited into colliding with a wildspire, momentarily getting Diablos stuck. \nDiablos is most powerful at the start of the fight. An effective strategy is to kite it around the arena, tiring it out. It is much slower and far less aggressive while exhausted, making the fight much easier.",
            },
            "Dodogama": {
                "weakness": "Water/Ice",
                "resistant": "Fire",
                "habitat": "Elder's Recess",
                "strategy": "Exploit Dodogama's vulnerability by directing attacks at its lower jaw when laden with rocks – sufficient damage triggers an explosion, toppling the monster and providing a strategic advantage. \nTo counter the threat posed by Dodogama molten assaults, execute a series of consecutive rolls. This agile maneuver will effectively mitigate both fire damage and the lingering Blast Blight status. Look at the status symbol hovering above your health bar; its disappearance signals your successful evasion. During its rolling attack – relocate to the front or rear of the monster to circumvent damage zones and potential knockback. \nExploit Dodogama's elemental weakness by using Thunder-based attacks, capitalizing on its high vulnerability to such damage.",
            },
            "Ebony Odogaron": {
                "weakness": "Ice",
                "resistant": "Fire",
                "habitat": "entire map",
                "strategy": "The Ebony Odogaron can shoot out energized dragon orbs from its mouth while in frenzy. You can try to shorten this period by hitting its head, however, if you get hit by the orb, it can nullify your elemental attacks. You have to be careful not to get hit while aiming for its head. It's ideal to do this from a distance, or do it only if you're super confident with your movement. \nDon't stand right in front of its face but aim for the head if possible. Your second target should be the tail. Try and keep the Ebony Odogaron from eating mid-combat. It goes into a frenzy right after eating and will make him more unpredictable in combat.",
            },
            "Fatalis": {
                "weakness": "Dragon",
                "resistant": "Fire",
                "habitat": "Castle Schrade",
                "strategy": "Facing the legendary black dragon, Fatalis, demands a keen understanding of its strengths and vulnerabilities. Being immune to stun, Fatalis requires a strategic approach. \nThe battle with Fatalis unfolds in distinct phases, each marked by devastating nova attacks. The initial nova occurs when Fatalis loses around 22% of its health, prompting hunters to seek shelter. Subsequent novas, triggered at different health thresholds, demand strategic positioning and evasive maneuvers. \nPrioritizing the breaking of Fatalis's head is crucial to weaken its attacks in the third phase. The arena provides numerous siege weapons, including cannons, ballistae, a roaming ballista, and the Dragonator. Coordinated use of these resources, along with Heavy Artillery to boost siege weapon damage, can create crucial openings for sustained attacks. \nBecause Fatalis is the hardest fight in the game, it is not recommended to tackle it until you have access to a fully optimized endgame setup, if possible with health augment for melee weapons (only unlocked after MR100 for R12 weapons).",
            },
            "Frostfang Barioth": {
                "weakness": "Fire/Thunder",
                "resistant": "Ice/Water",
                "habitat": "Hoarfrost Reach",
                "strategy": "Frostfang Barioth is a formidable opponent, boasting a variety of ice-based attacks. Equip armor with high ice resistance to mitigate damage from Frostfang Barioth's ice attacks. Use weapons with fire or thunder elemental damage to exploit its weaknesses and deal increased damage. Focus on attacking its head and tail for maximum damage. Breaking Frostfang Barioth's parts weakens its attacks and creates openings for additional damage. Aim to break its head, arms, and tail during the fight. \nUse the clutch claw to soften Frostfang Barioth's parts and create additional damage opportunities. Be prepared to dodge its charging attacks and icy projectiles. Position yourself strategically to avoid its attacks and create openings for counterattacks. Utilize the environment to your advantage, using slopes and ledges to mount Frostfang Barioth and deal additional damage.",
            },
            "Fulgur Anjanath": {
                "weakness": "Water/Ice",
                "resistant": "Thunder",
                "habitat": "entire map",
                "strategy": "Beware of Thunderblight, an ailment inflicted by Fulgur's electric assaults, increasing the risk of stunning hunter with rapid attacks. Fulgur Anjanath's thunder-infused attacks pose a significant threat, particularly its shocking bites that can swiftly deplete your health. It often strings these bites into combos, making it crucial to stay beneath or behind the monster for safety. Engaging cautiously, seize opportunities to strike, especially after it employs ranged electrical attacks. \nHis uncharged section is not nearly as dangerous as his charged state. Stamina Thief can slow him down in his charged mode so you can get in those precious damage numbers. If you use Stamina Thief, Ice element weapons are probably the best, since you can keep him in his uncharged state more often than not. ",
            },
            "Furious Rajang": {
                "weakness": "Ice",
                "resistant": "Fire/Thunder/Dragon",
                "habitat": "Hoarfrost Reach",
                "strategy": "Hunters must brace for an intensified onslaught, featuring lightning-fast punches, powerful beam attacks, and relentless pursuit. The Furious Rajang's frenetic combat style demands exceptional reflexes and strategic planning. Engaging this electrified behemoth requires hunters to stay on their toes, exploiting openings while mitigating the risks posed by its amplified rage. \nFurious Rajang does not have a tail (which is why it is Furious) and thus its only weakpoint is its arms/head, which can be hard to hit, tenderizing it's hindlegs can be extremely useful but difficult to manage considering how aggressive this monster is in shaking you off. \n Furious Rajang will destroy Shock Traps during rampage mode(red arms), will ignore Pitfall Traps when not enraged and can still attack out of a Pitfall Trap. \nIt is definitely recommended to avoid getting pinned, since Furious Rajang's pin attack will easily deal more than 50% of your health (with Health Boost 3) and knock you down, inflict Thunderblight, and most likely Stun. Using a Flash Pod on Furious Rajang while someone is pinned will free the pinned hunter.",
            },
            "Glavenus": {
                "weakness": "Water",
                "resistant": "Fire",
                "habitat": "Ancient Forest/Wildspire Waste/Elder's Recess",
                "strategy": "The recommended strategy involves utilizing Clutch Claw weapon techniques to erode its armor, seizing moments to retaliate after it executes various maneuvers. \nExercise caution during the tail slam maneuver. Glavenus, after slamming its tail behind, initiates a fiery spin with a wide reach. Maintain a safe distance or swiftly dash to the rear of its legs to evade the tail swipe. The tail slam has minimal setup, but the tail briefly rises before the slam. Effective evasion can be achieved through well-timed sidesteps. \nStay alert when Glavenus opens its mouth, signaling an impending bite with its fiery jaws.Be wary of a cunning move where Glavenus bites its tail before unleashing a charged spin with considerable reach. To avoid this, keep a safe distance, adhere closely behind its left leg, or execute a precisely timed dive. \nUse Fireproof, Vitality, or Temporal Mantles for fire damage and Fireblight Resistance.",
            },
            "Great Girros": {
                "weakness": "Fire",
                "resistant": "Water",
                "habitat": "Rotten Vale",
                "strategy": "This monster is adept at inducing paralysis with its venomous attacks. While lacking the imposing size of some counterparts, Great Girros poses a unique threat with its toxic assaults. Hunters must exercise caution, as paralysis can leave them vulnerable to subsequent attacks from both Great Girros and its subordinate pack. Staying vigilant, countering its venomous effects, and strategically targeting its parts are crucial tactics for a successful encounter with this unsettling creature. \nGreat Girros' paralysis-inducing attacks can be mitigated with the appropriate gear and consumables. Equip armor with high resistance to paralysis and bring Nulberries to counter the effects of paralysis.",
            },
            "Great Jagras": {
                "weakness": "Fire",
                "resistant": "Water",
                "habitat": "Ancient Forest",
                "strategy": "Great Jagras is a relatively low-level monster, making it an ideal target for hunters looking to hone their skills. Its straightforward combat style and predictable patterns provide an excellent opportunity for practice and experimentation. Hunters can test different weapons, tactics, and strategies against Great Jagras to refine their combat abilities and prepare for more challenging encounters. \nGreat Jagras' relatively low health and damage output make it an accessible target for hunters of all skill levels. Easier to defeat when they are famished, as they are smaller. If they have eaten, they will use their prey's added weight to put further force into its attacks.",
            },
            "Jyuratodus": {
                "weakness": "Thunder/Water",
                "resistant": "Fire",
                "habitat": "Wildspire Waste",
                "strategy": "Engaging Jyuratodus demands strategic targeting, as exploiting its vulnerability during mud phases becomes pivotal for a successful hunt in the swampy terrains of the New World. Uses mud for protection, resistances are INVERTED when covered in mud. The mud can be removed by shooting it with Puddle Pod ammo.",
            },
            "Kirin": {
                "weakness": "Fire",
                "resistant": "Thunder",
                "habitat": "Coral Highlands",
                "strategy": "Hunters must exercise caution, as Kirin's attacks can cause Thunderblight, and its swift movements make it a formidable adversary. Confronting Kirin requires not only strategic planning, but also mastery over dodging its electrifying assaults. Enraged by calling lightning from the sky, its body then deflects attacks; its attack pattern become more unpredictable and widespread. Only the horn is vulnerable.",
            },
            "Kulu Ya Ku": {
                "weakness": "Water",
                "resistant": "nothing",
                "habitat": "Ancient Forest/Wildspire Waste",
                "strategy": " Most of his attacks do minimal damage, so taking him out shouldn’t give you too much trouble. Keep a lookout for when he digs up a rock from the ground. He will try to use it to pound you with jump attacks and slam attacks. Do enough damage and you’ll force him to drop it. Keep an eye on your health and you should take this bird out no problem. ",
            },
            "Kulve Taroth": {
                "weakness": "Ice",
                "resistant": "Fire/Thunder",
                "habitat": "Caverns of El Dorado",
                "strategy": "Kulve Taroth spits out fire down the line, and there are also plenty of lava hazards. Make sure your Fire Resistance is decent. \nKulve Taroth is weak to Ice, so bring a weapon with Ice damage. \nKulve Taroth is a siege monster, so you will need to work with other players to defeat it. The goal is to break its horns, which requires a coordinated effort. \nKulve Taroth has a gold coat that can be broken off to reveal its true form. This is done by dealing enough damage to its coat. \nKulve Taroth has a variety of attacks, including a tail swipe, a fire breath attack, and a charge attack. Be prepared to dodge these attacks and counter with your own. \nKulve Taroth can also summon lava pools that can damage you if you step in them. Avoid these pools and focus on attacking Kulve Taroth.",
            },
            "Kushala Daora": {
                "weakness": "Thunder",
                "resistant": "Ice/Water",
                "habitat": "Ancient Forest/Elder's Recess",
                "strategy": "Kushala Daora is weakest in the head, followed by the forelegs and tail. All of them can be broken. Equip armor with high wind resistance to mitigate damage from Kushala Daora's wind attacks. Use weapons with thunder or dragon elemental damage to exploit its weakness and deal increased damage. Hunters must contend not only with its mighty breath attacks but also with the protective wind barrier that shields it from harm. \nThe Hunting Horn melody Wind Pressure Negated can be used to similar effect as described of Windproof III above. The melody All Wind Pressure Negated can be used to counter both normal air attacks and those of its enraged mode. \nEasiest way to defeat is to bring flash pods and 10 flash insects, wait until he flies and flash him, he will fall to the ground and be open.",
            },
            "Lavasioth": {
                "weakness": "Water",
                "resistant": "Fire/Thunder/Ice",
                "habitat": "Elder's Recess",
                "strategy": "Hunters should target the head and underbelly, identified as vulnerable areas. It is equipped with a magma layer that deflects attacks when cooled. To remedy this, apply Fire damage, utilizing slinger Torch Pods found in Lavasioth's locations. Alternatively, wait for Lavasioth to swim through magma, naturally softening its defenses. \nTo streamline your approach, equip your Palico or Kinsect with Fire weapons. This allows you to concentrate on carrying the most effective Water setup for maximizing damage. \nExercise caution with melee attacks unless you have specific tactics for softening the magma or attacking through it, such as employing abilities like Mind's Eye Ballistics or Spirit slash from Long Swords.",
            },
            "Legiana": {
                "weakness": "Thunder/Fire",
                "resistant": "Ice",
                "habitat": "Coral Highlands/Hoarfrost Reach/Guiding Lands",
                "strategy": "Legiana is weakest in the head, followed by the wings and tail. All of them can be broken. Equip armor with high ice resistance to mitigate damage from Legiana's ice attacks. Use weapons with thunder elemental damage to exploit its weakness and deal increased damage. \nLegiana is known for its aerial prowess, executing swift and precise attacks from the skies. To counter this, hunters must anticipate its movements and utilize ranged weapons or well-timed attacks to ground it. Use Nulberries to remove iceblight and maintain mobility during the fight.",
            },
            "Lunastra": {
                "weakness": "Ice/Dragon",
                "resistant": "Fire",
                "habitat": "Elder's Recess/Wildspire Waste",
                "strategy": "Using the Fireproof Mantle  is recommended for this fight.  Blue flames do not apply fire blight, but they do heat damage. Lunastra heats the air around her enough that cool drinks are required to prevent damage from the air. Her supernova attack has very large range and blasts twice. There is a special bond move where she combines her blast with Teostra to blast three times with a larger range and damage. Use Astera Jerkey after her first nova blast to heal red health on your bar and increase recovery. If Nergigante appears there is a rare turf war that does approximately 2000 damage to Lunastra. Kushala Daora can also have a turf war with her that does approximately 3000 damage to both participants. Use these to your advantage when fighting her. \nAim for her wings when she is downed if using a sever damaging weapon, which is her highest weak-point for those types of weapons while using blunt for head. \nOn top of shielding you from Lunastra's heat aura, Heat Guard will also protect you from the puddles of fire it puts on the floor, but it will not protect you from Fireblight.",
            },
            "Namielle": {
                "weakness": "Fire",
                "resistant": "Water/Thunder",
                "habitat": "Coral Highlands",
                "strategy": "Ranged weapons work best. Elemental weapons are specially effective. The fight might be easier with Health Boost 3, Divine Blessing, and Stun Resistance. Using vitality mantle and temporal mantle is advised. \nf you notice the camera zooming out, drop everything and start running. That's the Supernova and its almost guaranteed a oneshot if you're caught in it.",
            },
            "Nargacuga": {
                "weakness": "Thunder",
                "resistant": "Water",
                "habitat": "Ancient Forest/Coral Highlands",
                "strategy": "Nargacuga relies on his lightning speed and can hit a lot harder than its size. It's recommended to add Evade Extender and Flinch Free, through your Armor or Charms. Any armor will work against Nargacuga. \nNargacuga may pause and exit combat, sniffing the air and moving passively, as if to be searching for food. Then is a good time to Clutch Claw onto its face/tail and do a good amount of damage. \nListen for the audio cue of a low roar, this is followed up by a tail slam attack which can cause a lot of damage. \nDual Blades are recommended for this monster due to their quick attacks and dodges. Getting underneath Nargacuga and attacking is also effective.",
            },
            "Nergigante": {
                "weakness": "Thunder",
                "resistant": "Fire/Water/Ice",
                "habitat": "Elder's Recess",
                "strategy": "The key element of fighting Nergigante is keeping an eye on the spikes that periodically grow on its body. These spikes appear on four areas: Wings, Forelegs, Head, and Tail. When the spikes first grow, they have a yellow/white color and are a breakable weak spot. \nAs time passes, the spikes will harden and turn black. After this point, they are no longer a weak spot and may deflect attacks. Spiked body parts will do increased damage, and some attacks will be augmented by the spikes. \nOnce Nergigante has grown spikes on its head, wings, and forelegs, it will perform a dive bomb attack. And when the spikes turn into black, it will also launch the spikes upon hitting the ground. The best method of dealing with this attack is sprinting directly to either side and performing a leaping dodge just before Nergigante begins its dive. Due to this attack's massive area of effect, normal dodges are not sufficient for escaping damage. Nergigante is mildly susceptible to all ailments. Using weapons that can stun, paralyze, or cause sleep can buy a few moments to heal/sharpen/buff during the fight.",
            },
            "Odogaron": {
                "weakness": "Ice",
                "resistant": "Dragon",
                "habitat": "Coral Highlands/Rotten Vale",
                "strategy": "Odogaron is weak to Ice, so bring a weapon with Ice damage. Odogaron is a fast and aggressive monster, Odogaron's nasty claws cause heavy BleedingBleeding and should be avoided at all costs. Use meat to lure it into traps, stagger it, or coerce it into bouts of rage to tire it out and make it easier to deal with. \nBreaking a part and staggering it will cause it to counter-attack. So dodge right after. The Odogaron's tail has a really weird hitbox when it does its jumping back tail swipe move, so 90 percent of the time you will not get hit by it.",
            },
            "Paolumu": {
                "weakness": "Fire/Thunder",
                "resistant": "Water",
                "habitat": "Coral Highlands",
                "strategy": "Paolumu can't move around as freely when its air sacs are deflated. Aim for its inflated body parts, or purposefully draw out its attacks that use up stored air, to gain the upper hand. When Paolumu leaps into the air and performs a diving attack, attempting to land on hunters. Evading to the side or using terrain strategically is necessary to avoid getting hit by this aerial assault. \nThe Head and Mane are the weakest points",
            },
            "Pukei-Pukei": {
                "weakness": "Thunder",
                "resistant": "Water",
                "habitat": "Ancient Forest/Wildspire Waste",
                "strategy": "Pukei-Pukei is weak to Thunder, so bring a weapon with Thunder damage. Pukei-Pukei is a relatively low-level monster, making it an easy target for hunters looking to farm materials. Its straightforward combat style and predictable patterns provide an excellent opportunity for practice and experimentation. \nAim for the tail to cut it off and the head to deal the most damage. Pukei-Pukei's tail can be severed, reducing its range of attacks and providing additional rewards. When Pukei-Pukei is preparing to spit poison, aim for its head to interrupt the attack and create an opening for damage. \nMake sure to bring Antidote and Herbal Medicine with you.",
            },
            "Radobaan": {
                "weakness": "Dragon/Ice",
                "resistant": "nothing",
                "habitat": "Rotten Vale",
                "strategy": "Attack it as it rolls around to throw it off balance and knock it down. There is a small window of opportunity while it is rolling, during which any attack landed on the monster will result in a guaranteed knock-down. In order to know when you can attack it for a guaranteed knock-down, pay attention to its rolling animation. A couple seconds before it finishes its rolling sequence, it will start to slow down, and its body will start to wobble, and it will almost appear to be moving in slow motion. Attacking the monster while it is wobbling like this will cause it to lose its balance 100 percent of the time. Shattering its bone armor is the key to winning a fight against this beast.",
            },
            "Raging Brachydios": {
                "weakness": "Water/Ice",
                "resistant": "Fire",
                "habitat": "Guiding Lands",
                "strategy": "Unless you want to heal or retreat to get more Supplies, DON'T BACK UP. Raging Brachydios has three extremely long range attacks with large hitboxes and huge damage. Staying close to it and chipping away at its legs and fists is much safer. \nWhen enraged, All Areas of its body immediately switch to Flashpoint Slime. Glows stronger and coats area with slime, areas of the body will glow red including arms, head, shoulders, back, and the end of its tail. This is also a warning sign that its attacks will cause explosions on impact. Hitting slime lodged on its body with Watermoss or Slinger Bombs can dislodge them. Watch out as this will leave an explosive Slime Puddle underneath the part, that explodes after roughly 2 Seconds. \nHealth items including Max Potions, Lifepowders, and Dust of Life to heal you and your teammates, Cool Drink to prevent heat damage from the volcanic area and reduce the heat damage caused by the heated slime secreted by the monster during its final battle phase. \nRaging Brachydios' mechanics completely change in its last phase. Instead of just punching you, Raging Brachydios is mostly focused on spreading its completely released Flashpoint slime all over the Area. The slime deals much more damage on contact in this phase. Once a lot of slime is spread, the Raging Brachydios will roar, detonating every puddle of slime in the room. The explosion is so violent it even damages the Raging Brachydios",
            },
            "Rajang": {
                "weakness": "Ice",
                "resistant": "Fire/Thunder/Dragon",
                "habitat": "Guiding Lands",
                "strategy": "Rajang doesn't really have a wide, elegant moveset, but he compensates by dealing some of the highest damage in Monster Hunter World. Health Boost 3 is highly advised, especially when hunting in a group. \nRajang, faster and more relentless than it initially seems, outpaces many aggressive monsters like Nargacuga and Tigrex. This is attributed to its persistent charges and long-range lightning breath attacks. When it enters Rampage Mode, essentially a heightened state of rage, Rajang becomes even more ferocious, making frontal assaults a risky proposition. Rajang has no moves that directly target someone behind him. Standing at Rajang's rear end will be relatively safe. However, Rajang can turn or jump at any moment, so be on guard.",
            },
            "Rathian": {
                "weakness": "Dragon/Thunder",
                "resistant": "Fire",
                "habitat": "Ancient Forest/Wildspire Waste",
                "strategy": "Maneuvering around Rathian poses a significant challenge due to her potent tail venom and the extensive reach of her sweeping attacks. Creating a safer space becomes feasible by strategically severing her tail. When facing Rathian, equip fire-resistant armor to mitigate the impact of her venomous assaults. \nThe spikes on Rathian's tail harbor a formidable venom. However, this poison loses its efficacy when her tail is severed. Targeting her head during a hunt is a wise strategy, exploiting its vulnerability for a more effective offensive approach.",
            },
            "Ruiner Nergigante": {
                "weakness": "Dragon/Thunder",
                "resistant": "Fire/Water/Ice",
                "habitat": "Guiding Lands",
                "strategy": "The Ruiner Nergigante is the stronger and more ferocious version of the standard Nergigante. It shares a lot of its combat moves, speed, and behavior with the original, as well as having the ability to heal itself and resist damage as the fight wears on. As you first encounter the Ruiner Nergigante, you will immediately notice the white spikes that have formed on its limbs. At this state, these are its weakest points and you should aim for them. As you notice the spikes turn a different color, either black or metallic, the Ruiner Nergigante will start doing a Nose Dive attack. This is extremely dangerous and can cart players if it lands on your directly. Be ready to do an Emergency Dive if you think you will not make it to a safe zone. Ideally, you would want to equip the Rocksteady Mantle, or the Temporal Mantle to boost your chances of surviving the attacks. \nBe patient and keep an eye out for openings. Take out the spikes first while it's breakable and then focus next on the Head and Forearms. This will tenderize the body parts and will allow you to deal the most damage later on.",
            },
            "Safi'jiiva": {
                "weakness": "Dragon",
                "resistant": "Fire",
                "habitat": "Secluded Valley",
                "strategy": "Safi'jiiva is a siege monster, so you will need to work with other players to defeat it. The goal is to break its parts and weaken it, which requires a coordinated effort. \nSafi'jiiva's attacks are mostly elementless, even the beams. The only elemental attacks are the flame left on the ground after Safi'jiiva uses its thinner beams, which also causes Fireblight. Investing in Fire Resistance is thus not as useful as in the fights with monsters directly dealing fire attacks, such as Kulve Taroth. \nSafi'jiiva's limbs will always tenderize after one Clutch Claw weapon attack, no matter the weapon used even if you're not using Clutch Claw Boost. \nPoison and Blast both deal extra damage to Safi'jiiva. However, Poison doesn't contribute to part breaking. Hunters can bring Poison Smoke Bombs to inflict Poison on Safi'jiiva and save their weapons for part-breaking purposes.",
            },
            "Savage Deviljho": {
                "weakness": "Dragon/Thunder",
                "resistant": "Ice",
                "habitat": "entire map",
                "strategy": "Savage Deviljho is a variant of the standard Deviljho, boasting increased aggression and ferocity. Its attacks consist of lunging and chomping followed by stomping. As soon as you recognize this combo, get in position to just avoid the first chomp. For an easier chance to Flinch shot him, bring anything that causes Sleep since it is weak to sleep and avoid its enranged state by avoiding using big bombs. If you're directly ahead, you should already be out of range for the stomp attack. You can easily deliver an uppercut with any weapon, stabbing up at its head just after the chomp action is completed, giving you an opportunity to knock it. Once it gets up, the second phase will begin and it will start to swipe, deal a charged breath attack, and deal its famous pin attack. He starts to roll across the arena and can even leave a trail of dragon element that linger on the ground after its breath attack. This will afflict you with Dragon Blight so avoid getting caught in this and run to the side as soon as you recognize this attack beginning.",
            },
            "Seething Bazelgeuse": {
                "weakness": "Ice",
                "resistant": "Fire/Water",
                "habitat": "Elder's Recess",
                "strategy": "Seething Bazelgeuse will have a similar action set to the regular Bazelgeuse, except its scales will detach and it is able to fling them in different directions before they explode throughout the fight forcing you to maneuver out of its way as it creates a minefield. Seething Bazelgeuse attacks are generally telegraphed which will allow you to anticipate his next attacks and position yourself accordingly. He will be regularly lunging and charging ahead throughout the fight and the easiest way to avoid damage while remaining in close proximity is to roll through the underbelly area as it starts to move. \nOne massive attack to watch out for is its large ultimate dive attack. This attack is also telegraphed. You will be able to see as it flies directly upward while still shedding its explosive scales. This is before he begins his dive. Run out of harm's way before they start to explode and watch for when the Seething Bazelgeuse dives back down to the center which will initiate a secondary large explosion. If he's already diving, you may need to dive out of the landing area to gain as much distance as you can. As soon as it lands, you can begin running back in and continue your flurry of attacks.",
            },
            "Shara Ishvalda": {
                "weakness": "Ice/Water",
                "resistant": "Thunder/Fire",
                "habitat": "Origin Isle",
                "strategy": "Avoid using Lance or Gunlance weapons as this will pose more of a challenge during the second phase when going against the laser attacks. Use Damage Up and Crit Boost to maximize damage as much as possible, since players tend to run out of time during Combat even when hold up well. \nThere are rocks and boulders in the arena that can be knocked on the Shara Ishvalda. This will successfully knock him down while dealing a great amount of damage. This is most effective once you have softened his hide. \nIn Phase 2, you will need to watch for when to steer clear of his head area, since he has a new last beam attack. To continue your attacks on its head, keep to the side or clutch onto it from the side until his laser attack begins. Overall, you will need to watch the ground for his next moves and to watch out for sand puddles. Focus on getting a break and knocking it over to optimize all your attacks and its damage intake.",
            },
            "Shrieking Legiana": {
                "weakness": "Thunder/Fire",
                "resistant": "Ice",
                "habitat": "Hoarfrost Reach",
                "strategy": "A lot of its moves are similar to the Legiana, with the addition of its icy attacks and the Shrieking Legiana also roars (or shrieks) more frequently than the regular one. One of the things to watch out for when fighting the Shrieking Legiana is the Iceblight Ailments, so you'll be needing to adjust your Equipment accordingly. \nFor Decorations, use the Ice Resistance and Vitality Jewel to ensure that you will have a good chance at surviving the Shrieking Legiana's attacks. The ideal element to use against the Shrieking Legiana is Fire, followed by Thunder. It is also highly vulnerable to Poison attacks so you can also consider using poisonous weapons when you're playing with a party, or equip it on your Palico. \nThe weak point of a Legiana is the Head. You can use any of the damage types: Cut, Blunt, or Ammo to break it. Ideally, you want to deal the most damage when the Shrieking Legiana is not in its enraged state. You will have more opportunities to attack, and the Ice Blight attacks aren't as frequent. When the Shrieking Legiana takes flight, fire a Flash Pod directly in front of it to bring it down. This is especially helpful if you are using melee weapons to take the fight back to the ground.",
            },
            "Stygian Zinogre": {
                "weakness": "Thunder",
                "resistant": "Water/Ice/Fire/Dragon",
                "habitat": "Guiding Lands",
                "strategy": "Stygian Zinogre is susceptible to elemental damage, especially thunder. Equip a Thunder element weapon to maximize your damage output during its charged-up state \nPerform a diving dodge move when Stygian Zinogre unleashes its powerful Energy Blast. This not only helps you avoid the attack but also presents an opportunity to redirect the blast back to the monster, dealing additional damage. Stay close to the monster's side during its charged-up state to avoid lunging attacks. This positioning not only ensures your safety but also sets the stage for counter-attacks. \nUse the Clutch Claw to execute a Flinch Shot in response to Stygian Zinogre's aggressive movements. This technique capitalizes on the monster's momentum, bringing it down and creating openings for powerful combos. \nCarry Nulberries to counteract the effects of Dragonblight promptly.",
            },
            "Teostra": {
                "weakness": "Water/Ice",
                "resistant": "Fire",
                "habitat": "Wildspire Waste/Elder's Recess",
                "strategy": "Hunters should aim for the head, its weakest spot. Other weakspots are the wings and tail (which is severable). Since this is an agile monster, the belly area is the easiest to position oneself in. \nAt some points in the fight, Teostra will become covered in flames around its body. After some time he will take to the skies and release an explosion. The explosion covers a great distance so run away once he begins to fly up or utilize a flash pod to knock him to the ground. You can also utilize crystalburst to interrupt his supernova. \nHeat Guard can be extremely useful against Teostra, since it nullifies the damage from it's fire aura, and from the puddles of fire it drops on the floor",
            },
            "Tigrex": {
                "weakness": "Thunder/Dragon",
                "resistant": "Fire",
                "habitat": "entire map",
                "strategy": "Tigrex is a fast and aggressive monster, so it's important to stay on the move and avoid getting cornered. When its slowing down, either run away or get ready to dodge the finisher. \nTo best avoid its charge, run away perpendicular to Tigrex's charge. While Tigrex is turning, try to gain some distance from it and then repeat.Baiting Tigrex to charge into the ice pillars in the hoarfrost reach or the rock pillars in the Wildspire waste will result in it getting stuck, providing a short damage opportunity. Watch out though as the pillar will shatter once Tigrex breaks free, potentially flinching you",
            },
            "Tobi-Kadachi": {
                "weakness": "Water/Ice/Fire",
                "resistant": "Thunder",
                "habitat": "Ancient Forest",
                "strategy": "Tobi-Kadachi is weak to Ice, so bring a weapon with Ice damage. Strategic combat approaches involve targeting Tobi-Kadachi's head and tail weak spots. Advantageous results can be attained by breaking its head, spine, tail, and legs. Understand its bites, tail slams, and aerial attacks. Learn to evade and strike when it's distracted. Use Water Moss strategically.",
            },
            "Tzitzi-Ya-Ku": {
                "weakness": "Thunder/Ice",
                "resistant": "nothing",
                "habitat": "Coral Highlands",
                "strategy": "Tzitzi-Ya-Ku has the ability to perform a special attack where blinding light emanates from its head. This attack cannot be avoided by looking away from it. Instead, stay out of the stun range or block it with a shield. \nTzitzi-Ya-Ku's organs begin to radiate before it releases its blinding pulse, giving you enough time to escape and flank it. Damaging this organ will dramatically reduce the flash's effective range and can even nullify it entirely. \nAfter the flash attack, Tzitzi-Ya-Ku is momentarily vulnerable. Get close to its head, slightly off to the side, and unleash a combo while it recovers. The frills on its head are breakable, rendering the flash attack useless.",
            },
            "Uragaan": {
                "weakness": "Water",
                "resistant": "Fire",
                "habitat": "Elder's Recess",
                "strategy": "Start by gearing up with armor that has high thunder resistance to withstand its electric attacks. Equip a water or ice element weapon for better effectiveness against its tough hide. \nFocus on Uragaan's weaknesses to Water, Ice, and Dragon damage, targeting its head and underbelly. Break and mine its back, and cut off the tail for additional rewards.",
            },
            "Vaal Hazak": {
                "weakness": "Fire/Dragon",
                "resistant": "Water",
                "habitat": "Rotten Vale",
                "strategy": "The general tactics against Vaal Hazak is staying on its two sides (since it only has one breath ability that can attack sideways), maintaining a relatively close distance (since it has long distance reposition abilities that can put you in a position where it is impossible to be out of the line of fire of its breath), and keeping in mind that its charge abilities are (somewhat) wide and long. \nEnsure that your weapon is equipped with Fire or Dragon element, or opt for Blast or Stun if using an ailment. Select armor that prioritizes defense and elemental resistance, and always carry Mega Potions for healing during the fight. Additionally, Nullberries are crucial to counteract Vaal Hazak's gas attacks, and the Vitality Mantle can significantly reduce the damage taken. \nDue to its ability to shorten your Healthbar, a meal to get your Health up to 150, Vitality gems for up to 50 more HP, and a couple of Max Potions and Nutrients would be best to take on a hunt if you want to slay this Elder Dragon.",
            },
            "Velkhana": {
                "weakness": "Fire",
                "resistant": "Ice",
                "habitat": "Hoarfrost Reach",
                "strategy": "Velkhana primarily deals ice damage, so having armor with high Ice resistance can be beneficial. Also, consider using armor that provides skills such as Ice Resistance or Divine Blessing to mitigate damage. \nTo disrupt the Ice-covered Form, focus on breaking Velkhana's head or tail. Additionally, targeting the ice walls formed during its attacks provides opportunities for offense. Parts covered in ice become weak points, while the rest gains resistance, enabling hunters to optimize their damage output. \nWhen Velkhana takes to the air, a well-timed Slinger Burst can potentially ground it, unless it's in an enraged state. Dodge the sweeping ice beam attack by jumping off a small ledge or platform, using precise timing. The broken/melted ice walls leave behind platforms, offering opportunities for aerial attacks. Ensure you have an ample supply of healing items, such as potions and Mega Potions, to stay alive during the fight. Consider bringing Nulberries to remove the Iceblight status.",
            },
            "Viper Tobi-Kadachi": {
                "weakness": "Thunder",
                "resistant": "Water",
                "habitat": "Hoarfrost Reach",
                "strategy": "This version of Tobi-Kadachi can, on top of the regular moveset, shoots spikes from its tail that inflict both Poison and Paralysis. You can either get some Charms with resistance to nullify them, or be really fast with your food eating and bring Antidotes and Herbal Medicines instead. Depending on the resistances you bring to the fight be sure to choose wisely what parts to break first, the bite attack deals Paralysis while the tail is responsible for the Poison. Another thing to have in mind is its Thunder weakness, as always in this game preparation is key, so be sure to bring your most powerful weapon of this element. \nRegarding his attacks, one important thing to have in mind is that he roars before any of his movesets, you can negate this with Earplugs or a good enough roll, if you keep the fight in close quarters it will not have many chances to do the Paralysis Spikes attack.",
            },
            "Xeno'jiiva": {
                "weakness": "all elements equally",
                "resistant": "Sleep",
                "habitat": "Elder's Recess",
                "strategy": "Be very careful. As soon as it is in rage mode, its stomp becomes lethal once up close, since it adds an explosion after the initial stomp. Usually, when it isn't raging, the stomp is a good time to damage its feet, although its best to stay away from its front feet when it is in rage mode since anyone fighting with a close-range weapon will take heavy damage. \nXeno'jiva will fire three kinds of projectiles while grounded. The first will be three projectiles first firing middle then 45 degrees to the right then 45 degrees from center to the left. Its second is a 180-degree beam that is fired from its mouth covering the entire distance of the map. The third is just a straight beam that is fired directly in front of it (This is a very good time to do heavy damage near the side of its face and claws.) \nXeno'jiva beams will heat up the ground beneath it. A way to combat this is with Uragaan armour, the Heat Guard skill, or the Fireproof Mantle, as they will protect you from Fireblight.",
            },
            "Yian Garuga": {
                "weakness": "Water",
                "resistant": "Fire/Thunder/Ice",
                "habitat": "Guiding Lands",
                "strategy": "This fight may be scary for first timers as the monster is particularly aggressive and will do its attacks seemingly non-stop, the key to the fight is to identify the attacks that make him vulnerable like whis head plunge attack (be careful with this attack in particular since it deals the heaviest damage of its kit) and exploit them for maximum damage. You need to be constantly on alert and get damage in whenever possible. Be sure to hit its head as often as possible, since he is quite weak to stunning. You can deny its roars with Earplugs at level 5 and be sure to bring some Antidotes to deal with its poison. \nIn essence, cautious manoeuvring, constant vigilance, and strategic exploitation of opportunities are essential to win in this encounter.",
            },
            "Zinogre": {
                "weakness": "Ice/Water",
                "resistant": "Thunder",
                "habitat": "Ancient Forest/Guiding Lands",
                "strategy": "Beating Zinogre out of its charged state will also always end its enraged state. You may take advantage of that by enraging it while Zinogre is not charged, and to forcefully calm it down once it discharges. Target the front legs to induce staggering and create more opportunities for attacks. To evade its claws slams, simply dodge roll towards its tail. When it rolls in the air to shoot its lightning orbs, they seem to rotate in a counter clock wise direction.  If you are too close to it, they will hit you.  Distance is key to avoiding this attack.  Once the orbs have traveled a certain distance, they will dissipate. \nAs for equipment, Thunderproof mantle will help you avoid Thunderblight and high Level Earplugs (>3) will give you many more openings to deal damage, since this particular monster tends to howl a lot..",
            },
            "Zorah Magdaros": {
                "weakness": "Dragon/Water",
                "resistant": "Fire",
                "habitat": "Everstream",
                "strategy": "To optimize this bossfight and also to make sure you can do it if you are soloing, you should optimize your build to boost the damage to cannons and ballistae, Heavy Artillery 2 should suffice. Another important item to have is a Fireproof Mantle to survive damaging the cores. \nMost of the damage done to this boss will come from the cannons, so don't fret if you are dealing low dps when on top of it. Failing to destroy the cores in time will result in the boss erupting and dealing heavy damage. After destroying two cores while riding it, you will need to repel a Nergigante atop of it, so come prepared to take on that fight too. Ensure there is always someone prepared with either a binder or dragonator to counter Zorah's formidable magma attack. Remember to grab a binder from the ship and use the dragonator when Zorah Magdaros gets into range.",
            },
            # Possible to add more monsters if needed
        }

        monster_name = str(tracker.get_slot("monster"))

        # Use FuzzyWuzzy to account for misspellings/find the closest match
        best_match, score = process.extractOne(monster_name, monster_data.keys())

        # Only use the match if the score is above a certain threshold
        if score > 70:
            info = monster_data.get(best_match)
            response = f"{best_match} is weak to {info['weakness']} and resistant to {info['resistant']}. You can find it in the {info['habitat']}. To defeat it: {info['strategy']}"
        else:
            response = f"Sorry, I don't have any information about {monster_name}."

        dispatcher.utter_message(text=response)

        return [SlotSet("monster", None)]  # Reset the slot after providing the info


class ActionWeaponInfo(Action):
    def name(self) -> Text:
        return "action_weapon_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        weapon_data = {
            "Great Sword": {
                "description": "is a powerful weapon that deals massive damage with its charged attacks. It is slow but can stagger monsters and break parts easily. The True Charge Slash is the most powerful attack in the Great Sword's arsenal, dealing massive damage when fully charged. The weapon is best used by players who can predict monster movements and exploit openings",
                "strengths": "has high damage, good reach, can stagger monsters, can break parts easily.",
                "weaknesses": "has slow attack speed, limited mobility, requires good timing and positioning.",
            },
            "Long Sword": {
                "description": "is a versatile weapon that deals high damage with its Spirit Blade attacks. It has good reach and can perform quick combos to build up Spirit Gauge levels. The Spirit Helm Breaker is the Long Sword's most powerful attack, dealing massive damage when executed correctly. The weapon is best used by players who can maintain high Spirit Gauge levels and avoid getting hit.",
                "strengths": "has high damage, good reach, fast attack speed, Spirit Gauge mechanic.",
                "weaknesses": "it can trip teammates, requires good positioning, limited defensive options.",
            },
            "Sword and Shield": {
                "description": "is a fast and agile weapon that allows for quick attacks and good mobility. It can use items without sheathing the weapon, making it versatile in combat. The Perfect Rush combo is the Sword and Shield's most powerful attack, dealing high damage when executed correctly. The weapon is best used by players who can maintain a high tempo of attacks and adapt to different situations",
                "strengths": "has fast attack speed, good mobility, can use items without sheathing, versatile in combat.",
                "weaknesses": "has low damage per hit, limited range, requires good timing and positioning.",
            },
            "Dual Blades": {
                "description": "are fast and aggressive weapons that excel at dealing elemental damage and inflicting status effects. They have good mobility and can perform long combos to build up Demon Mode levels. The Demon Dance is the Dual Blades' most powerful attack, dealing high damage when executed correctly. The weapon is best used by players who can maintain high Demon Mode levels and exploit elemental weaknesses",
                "strengths": "has fast attack speed, good mobility, high elemental damage, can inflict status effects.",
                "weaknesses": "has low damage per hit, limited range, high stamina consumption.",
            },
            "Hammer": {
                "description": "is a heavy weapon that deals high damage with its charged attacks. It can stun monsters and break parts easily with its impact damage. The Big Bang combo is the Hammer's most powerful attack, dealing massive damage when executed correctly. The weapon is best used by players who can land charged attacks on monster heads and exploit stun openings",
                "strengths": "has high damage, can stun monsters, can break parts easily, good reach.",
                "weaknesses": "has slow attack speed, limited mobility, requires good timing and positioning.",
            },
            "Hunting Horn": {
                "description": "is a support weapon that can buff teammates with melodies and deal damage with its attacks. It has good reach and can perform long combos to build up melodies. The Echo Wave - Dragon is the Hunting Horn's most powerful attack, dealing high damage when executed correctly. The weapon is best used by players who can maintain melodies and support the team with buffs",
                "strengths": "has support abilities, good reach, can buff teammates, versatile in combat.",
                "weaknesses": "has low damage per hit, limited range, requires good timing and positioning.",
            },
            "Lance": {
                "description": "is a defensive weapon that excels at blocking attacks and countering with precise thrusts. It has good reach and can perform long combos to build up Guard levels. The Counter Thrust is the Lance's most powerful attack, dealing high damage when executed correctly. The weapon is best used by players who can maintain high Guard levels and exploit counter openings",
                "strengths": "has high defense, good reach, can counter attacks, versatile in combat.",
                "weaknesses": "has limited range, requires good timing and positioning.",
            },
            "Gunlance": {
                "description": "is an explosive weapon that deals high damage with its shelling attacks. It has good reach and can perform long combos to build up Wyrmstake levels. The Wyrmstake Blast is the Gunlance's most powerful attack, dealing massive damage when executed correctly. The weapon is best used by players who can maintain high Wyrmstake levels and exploit shelling openings",
                "strengths": "has high damage, good reach, can shell attacks, versatile in combat.",
                "weaknesses": "has low mobility, limited range, requires good timing and positioning.",
            },
            "Switch Axe": {
                "description": "is a versatile weapon that can switch between axe and sword modes to deal high damage. It has good reach and can perform long combos to build up Amped levels. The Zero Sum Discharge is the Switch Axe's most powerful attack, dealing massive damage when executed correctly. The weapon is best used by players who can maintain high Amped levels and exploit sword mode openings",
                "strengths": "has high damage, good reach, can switch between modes, versatile in combat.",
                "weaknesses": "doesn't have much mobility, limited range, requires good timing and positioning.",
            },
            "Charge Blade": {
                "description": "is a complex weapon that can switch between sword and axe modes to deal high damage. It has good reach and can perform long combos to build up Phial levels. The Super Amped Element Discharge is the Charge Blade's most powerful attack, dealing massive damage when executed correctly. The weapon is best used by players who can maintain high Phial levels and exploit axe mode openings",
                "strengths": "High damage, good reach, can switch between modes, versatile in combat.",
                "weaknesses": "Complex mechanics, high skill ceiling, requires good timing and positioning.",
            },
            "Insect Glaive": {
                "description": "is an agile weapon that can vault into the air and perform aerial attacks. It has good reach and can perform long combos to build up Kinsect levels. The Kinsect Extract is the Insect Glaive's most powerful attack, dealing high damage when executed correctly. The weapon is best used by players who can maintain high Kinsect levels and exploit aerial openings",
                "strengths": "High mobility, good reach, can vault into the air, versatile in combat.",
                "weaknesses": "Low damage per hit, limited range, requires good timing and positioning.",
            },
            "Bow": {
                "description": "is a ranged weapon that can deal high damage with its charged shots. It has good reach and can perform long combos to build up Charge levels. The Dragon Piercer is the Bow's most powerful attack, dealing massive damage when executed correctly. The weapon is best used by players who can maintain high Charge levels and exploit weak point openings",
                "strengths": "High damage, good reach, can charge shots, versatile in combat.",
                "weaknesses": "Limited ammo, requires good timing and positioning, limited range.",
            },
            "Light Bowgun": {
                "description": "is a ranged weapon that can deal high damage with its rapid shots. It has good mobility and can perform long combos to build up Special Ammo levels. The Wyvernblast is the Light Bowgun's most powerful attack, dealing high damage when executed correctly. The weapon is best used by players who can maintain high Special Ammo levels and exploit weak point openings",
                "strengths": "High damage, good mobility, can rapid shots, versatile in combat.",
                "weaknesses": "Limited ammo, requires good timing and positioning, limited range.",
            },
            "Heavy Bowgun": {
                "description": "is a ranged weapon that can deal high damage with its powerful shots. It has good range and can perform long combos to build up Special Ammo levels. The Wyvernheart is the Heavy Bowgun's most powerful attack, dealing massive damage when executed correctly. The weapon is best used by players who can maintain high Special Ammo levels and exploit weak point openings",
                "strengths": "High damage, good range, can powerful shots, versatile in combat",
                "weaknesses": "Limited mobility, requires good timing and positioning, limited range",
            },
        }
        weapon_name = str(tracker.get_slot("weapon"))

        # Use FuzzyWuzzy to account for misspellings/find the closest match
        best_match, score = process.extractOne(weapon_name, weapon_data.keys())

        # Only use the match if the score is above a certain threshold
        if score > 80:
            info = weapon_data.get(best_match)
            response = f"The {best_match} {info['description']} It {info['strengths']}, however it also {info['weaknesses']}."
        else:
            response = f"Sorry, I don't have any information about {weapon_name}. Try again with a different weapon."

        dispatcher.utter_message(text=response)

        return [SlotSet("weapon", None)]  # Reset the slot after providing the info


class ActionMechanicInfo(Action):
    def name(self) -> Text:
        return "action_mechanic_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        mechanic_data = {
            "Clutch Claw": {
                "description": "The Clutch Claw is a tool that allows hunters to grapple onto monsters and perform special attacks. It can be used to soften monster parts, create openings for attacks, and redirect monster movements. The Clutch Claw can also be used to wound monster parts, making them more vulnerable to damage. It is an essential tool for hunters looking to maximize their damage output and exploit monster weaknesses.",
            },
            "Elemental Damage": {
                "description": "Elemental damage is a type of damage that is inflicted by weapons with elemental properties. It includes Fire, Water, Ice, Thunder, and Dragon damage. Elemental damage can be used to exploit monster weaknesses and deal additional damage. Each monster has different elemental weaknesses and resistances, so it is important to use the right element against each monster. Elemental damage can be boosted with skills, armor, and decorations to maximize its effectiveness."
            },
            "Affinity": {
                "description": "Affinity, also known as Critical Chance, in Monster Hunter World (MHW) is a weapon's chance to deal a bonus or a penalty to Damage on attacks. Affinity is determined by the Weapon and Skills that are being used, and is displayed as a percent value in the Attack Status portion of the Equipment Info screen. At 0% Affinity there is no chance for a bonus or penalty to damage. A positive Affinity value denotes the chance for an attack to -crit-, which applies a bonus of 25% to Physical (Raw) Damage. A negative value, on the other hand, denotes the chance to -blunder-, which applies a penalty of 25% to Physical Damage. \nPlease note that Affinity ONLY applies to Raw Damage under normal circumstances. You must have the Critical Element skill active for it to apply to Elemental Damage"
            },
            "Sharpness": {
                "description": "Sharpness in Monster Hunter World (MHW) is a factor in determining the cutting power of a Weapon and its damage output. The Sharpness level of a weapon will degrade over the course of a fight. When wielding a Blademaster Weapon, it is important to keep it at its maximum Sharpness with Whetstones. This will make cutting Monster parts easier (blade weapons only) and lower the chance of an attack being deflected. In addition to reducing chance of deflection, Sharpness will also increase Raw (Physical) Damage and Elemental Damage. There are 7 levels of Sharpness. Damaging Monster parts sometimes requires a weapon to currently be at a certain level."
            },
            "Elderseal": {
                "description": "Elderseal is a Weapon Mechanic that prevents certain Elder Dragons from using their special aura abilities and enrage attacks as often."
            },
            "Gunlance Shelling": {
                "description": "Shelling is unique in that it can deal fixed damage to a monster's parts regardless of their defense. However, every shell consumes twice the amount of Sharpness compared to normal attacks. If Sharpness is below green (yellow and below), shelling damage is significantly reduced. Shells also cannot be fired in red Sharpness. Each Gunlance possess one of three different types of shells - Normal, Long, and Wide. The shell types differ in damage, ammo capacity, area of effect, and have different shelling bonuses. For example, Normal shells receive a bonus to Burst Fire, whereas Long shells have a bonus to Charged Shelling. In choosing your Gunlance, each type will require a slightly different play style."
            },
            "Charge Blade Phial": {
                "description": "Phials are a unique feature of the Charge Blade. They are used to store energy and release it in powerful attacks. The Charge Blade has two types of Phials - Impact and Element. Impact Phials deal stun damage and can KO monsters, while Element Phials deal elemental damage. Phials are charged by attacking with the sword and shield in Sword Mode, and can be released in Axe Mode to deal massive damage."
            },
            "Bowgun Ammo": {
                "description": "Ammo is the lifeblood of the Bowguns. It determines the type of damage you can inflict. Recover, Armor, and Demon rounds can heal and buff allies quickly and at a distance, while status inflicting rounds (especially Sleep and Paralysis rounds) can set a hunting party up for devastating co-ordinated attacks."
            },
            "Decorations": {
                "description": "In Monster Hunter World, Decorations empower hunters to create a personalized and formidable arsenal. These precious jewels, earned through challenging Quests and battles, can be slotted into armor to unlock powerful Skills. Crafting a synergistic combination of Decorations allows hunters to amplify their strengths and mitigate weaknesses. Whether aiming for increased damage, enhanced survivability, or specialized utility, the strategic use of decorations transforms armor sets into finely tuned instruments of destruction. Embracing the possibilities offered by decorations ensures that each hunter's gear is not just protective but tailored to their unique hunting style and preferences. \nDecorations can only be obtained by completing High/Master rank quests or by using the melding pot."
            },
            "Sleep": {
                "description": "Sleep is a Status Effect in Monster Hunter World (MHW). When Sleep is triggered, the Monster will topple over and remain asleep for about 40 seconds. Once the Monster is fully asleep, damage from any single source will be doubled and wake the Monster up, ending the effect. Triggering the effect requires buildup inflicted by: \nWeapons that wield Sleep damage \nBowgun Sleep Ammo \nBow Sleep Coating \nSleep Knives \nEnvironmental Hazards such as Sleeptoad"
            },
            "Traps": {
                "description": "Traps allow a Hunter to incapacitate a Large Monster for a short time, setting it up for Capture or an opportunity to go on the offensive. While caught in a Trap, a Monster can be captured if it is an a Weakened state - denoted by this minimap-icon-monster-status-weak symbol on the minimap when the Scoutfly Level for that Monster is at level 3. Using two Tranq Bombs, Tranq Knives, or Tranq Ammo rounds is enough to capture any Monster, before or after it is caught in a Trap."
            },
            "Capture": "Capturing a monster is an alternative way to complete a hunt in Monster Hunter World. To capture a monster, you must first weaken it until it starts limping away. Once the monster is weakened, you can set a trap and lure the monster into it. Once the monster is trapped, you can use Tranq Bombs to put it to sleep and complete the capture. Capturing a monster has the same rewards as slaying it, but it can be faster and more efficient in some cases.",
        }

        mechanic_name = str(tracker.get_slot("mechanic"))

        # Use FuzzyWuzzy to account for misspellings/find the closest match
        best_match, score = process.extractOne(mechanic_name, mechanic_data.keys())

        # Only use the match if the score is above a certain threshold
        if score > 70:
            info = mechanic_data.get(best_match)
            response = f"{info['description']}"
        else:
            response = f"Sorry, I don't have any information about {mechanic_name}. Try again with a different mechanic."

        dispatcher.utter_message(text=response)

        return [SlotSet("mechanic", None)]  # Reset the slot after providing the info
