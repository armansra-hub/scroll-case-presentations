#!/usr/bin/env python3
"""Verbatim self-check for horizon-retail.html: every popup / speech bubble /
in-scene text must contain its source strings, in order, unaltered.
Sources: Scenario 2.pdf and the user's spec."""
import re, html, sys

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "horizon-retail.html")
doc = open(TARGET, encoding="utf-8").read()

def block_text(elem_id):
    i = doc.index(f'id="{elem_id}"')
    start = doc.rindex("<div", 0, i)
    depth = 0
    j = start
    for m in re.finditer(r"<div\b|</div>", doc[start:]):
        if m.group(0) == "<div":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                j = start + m.end()
                break
    seg = doc[start:j]
    seg = re.sub(r"<svg.*?</svg>", " ", seg, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", seg)
    txt = html.unescape(txt)
    return re.sub(r"\s+", " ", txt).strip()

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

EXPECTED = {
"pp-email": [
"Subject: Re: Your Slope Line",
"Hi {Name},",
"I appreciate the direct response. If the full $250,000 is what you need right now, I understand why Onramp’s offer looks stronger.",
"Before you make a final decision, I think it would be worth taking 15 minutes to compare the two offers beyond the approved amount. The key differences are repayment structure, term length, total cost, and whether the capital is needed all at once or across multiple inventory cycles.",
"Slope’s line is smaller today, but it is revolving. You can draw what you need, repay it, and reuse the line without reapplying. Onramp’s offer may be the better fit if you need the full $250,000 immediately, but if the capital is being used across multiple purchases, Slope may be worth comparing more closely.",
"Do you have 15 minutes this week? I can walk through both structures with you and help determine which one fits your actual use case better.",
"Best,",
"{Signature}",
],
"pp-mental": [
"The first gate is whether they need $250K right now for one large purchase, or whether that is their total capital need across multiple buys over the next few months. If they truly need $250K immediately, Slope may not be the best fit for that specific event, and the honest move is to say so while keeping the Slope line open for future or parallel use. If their need is spread across multiple purchases, restocks, or inventory cycles, then Slope becomes much more competitive because the revolving structure, repayment flexibility, early repayment savings, and ability to reuse the line may create more value than a larger one-time advance.",
"From there, the key questions are about the Onramp terms, the actual use case, the purchase schedule, the cash conversion cycle, and the real cost of each product. The comparison should be: Onramp may be better for a single large immediate deployment, while Slope may be better for recurring working capital, faster inventory turns, better repayment alignment, and long-term capital access. Customer stories support this: Kanso for matching repayment to the working capital cycle, Continental Cards for evaluating financing based on inventory turns and structure, and National Bobblehead for line growth and trust.",
"The final strategy is truth-based selling. If Slope is better for their actual use case, show them why and close. If Onramp is better right now, be honest, preserve the relationship, and anchor a future Slope use case to a real date, like the next inventory cycle or when the Onramp advance is close to being repaid.",
],
"bub-gate": [
"Step 1: Qualify the capital need",
"“Is the $250K for one large purchase you need funded right now, or is that your total capital need over the next few months across multiple buys?”",
],
"pp-fork": [
"“Is $250K the exact amount required, or is that more of a comfortable buffer?”",
],
"pp-croc": [
"“Then I want to be straight with you. If you need the full $250K for one purchase right now, our $100K line may not cover that specific event. I would not want to force a fit where there is not one.”",
"Then ask:",
"“Is this a one-time purchase, or will there be follow-on restocks, supplier payments, or smaller buys after this?”",
"If truly one-time:",
"Onramp may be the better fit for that specific need. I would preserve the relationship, keep the Slope line open, and anchor a follow-up around a real future event. Dead end.",
"If part of a larger inventory cycle:",
"Slope may still be useful in parallel for restocks, smaller supplier payments, emergency flexibility, or capital needs after the Onramp term.",
],
"pp-oasis": [
"If they need over $100K but there is a buffer:",
"“If you have not already signed and committed to the $250K offer, I would recommend only taking the exact amount needed for the purchase with Onramp so you are not paying for capital you are not using. If you need more capital, you can draw from Slope whenever you want, choose your repayment schedule and terms, and only pay interest on the money you draw and the days you hold it.",
"Also, with additional paperwork, you may be able to qualify for a higher limit. Many of our customers have done the same. I would be happy to connect with internal resources and send over what we need. Would you be interested in that?”",
],
"bub-path2": [
"If the $250K is spread across multiple buys:",
"Slope is back in the conversation. The question becomes whether a $100K revolving line can service the actual purchase schedule better than a larger one-time advance.",
],
"pp-s2": [
"Step 2: Understand the actual Onramp terms",
"“Do you mind sharing what fee Onramp quoted you on the $250K?”",
"“And just to confirm, is it fixed weekly payments over 90 days, or is it tied to a percentage of sales?”",
"“If it is fixed weekly, have they shown you the actual weekly payment amount?”",
"Why this matters:",
"I cannot compare offers honestly without knowing the actual fee, repayment structure, and weekly payment. Those details determine the true cost of capital and whether the repayment schedule fits the way their business operates.",
"If they know the fee:",
"I can compare the actual cost against Slope.",
"If they do not know the fee:",
"I would walk them through the math:",
"250,000 × (1 + fee %) / weeks = weekly payment",
],
"pp-s3": [
"Step 3: Map the purchase schedule",
"“Walk me through the buys. Roughly how much do you need and when over the next 90 days?”",
"Why this matters:",
"This tells me whether they need $250K on day one or only need pieces of it at different times.",
"If they say:",
"“We need $80K now, $70K next month, and another $100K later.”",
"I would think:",
"Onramp gives them the full $250K upfront and charges based on the full advance. Slope lets them draw only what they need when they need it.",
"How I would position it:",
"“If your purchases are staggered, you would be paying their fee on $250K from day one even if you are only using part of it at the beginning. If you are buying $80K now, another $70K next month, and the rest later, you are still paying for the full $250K the entire time. With Slope, you draw what each purchase needs when it needs it. You only pay interest on the amount you actually use, once you repay your balance is replenished, and you can cycle through the line as many times as you need.”",
],
"pp-s4": [
"Step 4: Check the cash conversion cycle",
"“From wiring the supplier to Walmart paying you back, how many days does one cycle usually take?”",
"Follow-up if doing multiple purchases:",
"“Does the first purchase convert back into cash before the next purchase is due, or do those cash needs overlap?”",
"Why this matters:",
"The cycle length matters in two ways.",
"First, it tells me whether Slope’s $100K revolving line can be reused across multiple buys. If the first purchase converts back to cash before the next buy is due, Slope can compete hard because they can draw, repay, and reuse the same line instead of taking one large advance upfront.",
"Second, it tells me whether Onramp’s 90-day term matches their cash cycle. If the inventory takes 120 or 150 days to convert back into cash, Onramp may require weekly payments before the purchase has paid for itself. That means they are floating payments out of existing cash instead of revenue from the inventory being financed.",
"If the cycle is short enough:",
"Slope may be able to replace Onramp because the line can revolve across purchases.",
"If the cycle is longer than 90 days:",
"Slope may still compete hard because the repayment terms can better align to the actual inventory cycle.",
"If purchases overlap and the outstanding need is above $100K:",
"Slope may not fully replace Onramp, but it can still run in parallel for part of the need, future restocks, supplier payments, or flexibility after the Onramp term.",
"How I would position it:",
"“This is the key timing question. If your purchases turn quickly, Slope can be valuable because the line replenishes and can be reused. If your cycle is longer than 90 days, Slope can also be valuable because the repayment schedule may fit the inventory cycle better. Either way, I would want to compare the repayment timing against when the cash actually comes back into the business.”",
"Customer story:",
"Kanso is relevant here. Kanso used Slope to better align repayment with supplier terms and working capital timing.",
],
"pp-s5": [
"Step 5: Compare cost with their real numbers",
"I would not assume Slope is cheaper. I would run the comparison with their actual numbers.",
"Onramp cost:",
"Flat fee in dollars, fixed weekly payments, fee may not change if they repay early, and payment amount matters because it affects weekly cash flow.",
"Slope cost:",
"Draw amount × APR ÷ 365 × days held.",
"Interest is based on what they actually draw. First draw has 20% off interest. If they repay early, the cost decreases.",
"How I would position it:",
"“I would want to run this with your actual numbers. If Onramp is cheaper and the structure fits your cycle, I will say that. If Slope is cheaper or better aligned to how you are buying inventory, I will show you that clearly.”",
"If they say Onramp’s fee looks lower:",
"I would not argue from the headline number. I would ask for the fee, repayment timing, and how long they actually hold the capital. A flat fee can look cheaper upfront, but the real comparison depends on the total fee, weekly repayment burden, average capital actually used, and whether early repayment saves anything.",
"If they are using the full $250K immediately and the fee is low:",
"Onramp may be the better cost option for that specific event.",
"If they are using the capital in stages or turning inventory quickly:",
"Slope may be cheaper because they only pay on what they draw and for the days they hold it.",
],
"pp-s6": [
"Step 6: Only if it is earned, look for a margin opportunity",
"“Do your suppliers offer better pricing if you buy more or pay earlier?”",
"If yes:",
"The comparison is not just cost of capital. It is whether the capital helps them make more money than it costs.",
"How I would position it:",
"“If buying earlier or buying deeper gives you better supplier pricing, then the real question is whether the margin you capture is greater than the financing cost.”",
"Customer story:",
"Neato is relevant here. They used Slope to buy deeper, pay suppliers earlier, and improve margin after financing costs.",
"Slope’s longer payment terms could be a plus here.",
],
"pp-p1": [
"Fit to actual use case",
"If they need the full $250K immediately for one purchase, Onramp may be the better fit for that event.",
"If the need is spread across multiple buys, Slope may be the better structure because they can draw, repay, and reuse the line.",
],
"pp-p2": [
"Weekly repayment pressure",
"Onramp’s fixed structure means weekly payments start right away.",
"I would compare that payment against their Walmart payout timing and cash conversion cycle.",
],
"pp-p3": [
"Idle capital",
"If their purchases are staggered, Onramp may charge them on the full $250K even if they are only using part of it upfront.",
"With Slope, they only pay interest on what they draw and for the days they hold it.",
],
"pp-p4": [
"Reusability",
"Onramp is a larger one-time advance.",
"Slope is revolving, so as they repay, available credit replenishes and can be used again without reapplying.",
],
"pp-p5": [
"Term alignment",
"Onramp’s offer is 90 days.",
"If their inventory takes 120 or 150 days to convert back into cash, Slope’s longer available terms may better match the actual business cycle.",
"This is where I would reference Kanso, since they used Slope to better align repayment with supplier terms and working capital timing.",
],
"pp-p6": [
"Early repayment and actual cost",
"With Slope, cost is based on the amount drawn and days held.",
"If they repay early, the cost goes down.",
"With a flat-fee structure, early repayment may not create the same savings.",
"I would not assume Slope is cheaper. I would get Onramp’s actual fee and run the comparison honestly.",
],
"pp-p7": [
"Line growth",
"The $100K approval is not necessarily the ceiling.",
"If they use the line responsibly and build repayment history, there may be a path to a higher limit over time.",
"National Bobblehead is the relevant story here.",
],
"pp-p8": [
"Coexistence",
"This does not have to be either/or.",
"If Onramp is better for the immediate large purchase, Slope can still be useful as the standing line for future restocks, supplier payments, emergency flexibility, or the next cycle.",
],
"bub-bird": [
"What would make you believe the customer is still winnable?",
],
"pp-win": [
"They are still winnable because they replied instead of ghosting, and objections are engagement. Their issue is specific: Onramp approved more money. That gives me a clear problem to solve. They also have not drawn on either facility yet, so the decision is still open. If they are only comparing headline amount, there may still be an information gap around Onramp’s actual fee, weekly repayment, purchase timing, cash conversion cycle, and whether they truly need the full $250K at once. They came to Slope first, so the disappointment is also a buying signal. If they are willing to share the Onramp terms and walk through the numbers, then the deal is very winnable if Slope saves them money, makes them money, reduces repayment pressure, or better fits the way they buy inventory. Even if Onramp is better for the immediate purchase, Slope can still win later or in parallel because the line stays open for future restocks, supplier payments, emergency flexibility, or the next capital cycle.",
],
"walltext": [
"What would you emphasize besides line size?",
"I would emphasize the factors that determine whether the capital actually saves or makes Horizon money.",
],
}

# standalone scene labels (signposts, buttons)
PLAIN = [
"One large purchase",
"Total capital need",
"Exact amount needed",
"Comfortable buffer",
"Explore Path 1 first",
"GAME OVER?",
]

fails = 0
for pid, parts in EXPECTED.items():
    try:
        txt = block_text(pid)
    except ValueError:
        print(f"FAIL [{pid}] — element not found")
        fails += 1
        continue
    pos = 0
    for p in parts:
        n = norm(p)
        i = txt.find(n, pos)
        if i < 0:
            where = "out of order" if txt.find(n) >= 0 else "MISSING/ALTERED"
            print(f"FAIL [{pid}] {where}: {n[:90]}…")
            fails += 1
        else:
            pos = i + len(n)
full = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", doc)))
for p in PLAIN:
    if norm(p) not in full:
        print(f"FAIL [plain] missing: {p}")
        fails += 1

if fails:
    print(f"\n{fails} failure(s).")
    sys.exit(1)
print(f"All {len(EXPECTED)} stations + {len(PLAIN)} labels verbatim-verified ✔")
