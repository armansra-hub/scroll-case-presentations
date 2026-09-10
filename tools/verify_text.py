#!/usr/bin/env python3
"""Verbatim self-check: every station popup's text must contain the source
strings, in order, unaltered. Sources: Scenario 1.pdf (email, mental model,
positioning, first draw) and the user's spec (jumps, obstacles)."""
import re, html, sys

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "summit-commerce.html")
doc = open(TARGET, encoding="utf-8").read()

def popup_text(pid):
    i = doc.index(f'id="pp-{pid}"')
    # walk div nesting from the opening tag of the popup
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
"email": [
"Hi {Name},",
"Congratulations, Summit Commerce has been approved for a $250,000 revolving line of credit with Slope.",
"Here are the details of your approval:",
"Approved Line: $250,000",
"APR Range: 14% to 18%",
"Promotion: 20% off interest on your first draw",
"Supported by a J.P. Morgan credit facility, with loans originated by Lead Bank, Member FDIC",
"My name is Arman, and I will be your point of contact at Slope moving forward. I can help with any questions around your line, available terms, repayment schedule, first draw, or how to think through using Slope alongside your current financing options.",
"I would like to set up 15 minutes this week to introduce myself, walk you through how the line works, and make sure everything is ready when the timing makes sense for your business.",
"Are you available sometime Monday or Tuesday next week?",
"Best,",
"{Signature}",
],
"mental": [
"My mental model is that Summit Commerce is already a qualified, approved borrower, but they may still need help understanding Slope’s terms, how the line works, and how it compares to what they have used before. I would start by clearing up any confusion around the approval, APR, draw process, or repayment structure, then focus on their experience with Amazon Lending to understand where there may be pain around access, flexibility, repayment, or use of funds. From there, I would dig into what they originally wanted the $300K for, whether that need is still active, and whether drawing now makes sense based on a real business use case like inventory, supplier payments, PPC, product launches, buying deeper, or bridging Amazon payout timing.",
],
"j1": [
"Is there anything top of mind or any questions or concerns you have about your approval? Have you gotten a chance to look at it yet?",
"If they forgot about it:",
"No problem, that happens. The line is already approved, so I would just want to quickly walk you through how it works and see if there is a real use case where it makes sense.",
"If they are confused by APR or fees:",
"Totally fair. APR and total financing cost can be easy to mix up. I can walk you through the actual dollar cost of a sample draw so it is clear.",
"If they say no / nothing top of mind:",
"\"Okay awesome. Well, if you don't mind, I'd love to just learn a little more about you guys and the business. How did you get started doing this?\"",
"Potential follow-ups:",
"Take something from their story and tie it to growth question: \"Oh wow thats awesome, was there any ever growing pains as you guys were doing (xyz)\"",
"\"Have you guys used lending or financing at any point to support that growth?\"",
],
"j2": [
"How has your experience been with Amazon Lending?",
"Are you carrying any other financing right now?",
"Save this info for later, because Slope may be useful as a way to pay off higher-cost debt.",
"With Amazon Lending, has there ever been a time when you needed capital and were not able to get it?",
"When you are repaying, how does that work for you? Do you control the timing, or does it come out automatically?",
"During a slower week, does that ever create a cash flow pinch?",
"When you used Amazon Lending, were you able to use the money however you wanted, or was it more locked into Amazon-related expenses?",
],
"j3": [
"What have you typically used financing for?",
"Inventory?", "Supplier payments?", "PPC?", "Product launches?", "Covering timing gaps?", "Paying off another financing product?",
"What prompted the original $300K request?",
"Was that tied to inventory, supplier payments, PPC, a product launch, paying off another financing product, or something else?",
"Is that need still active, or has the timing changed since you applied?",
"When would you ideally want that capital available?",
"How often do you restock your main SKUs? 30 days? 60? 90?",
"Is that cadence the best operational decision, or is that mostly what cash flow allows?",
"What determines that number: demand, supplier terms, warehouse capacity, or available cash?",
"Do your suppliers offer better pricing if you place larger orders?",
"Do they offer early-payment discounts or better terms if you pay upfront?",
"Are there proven SKUs where you would buy deeper if the capital was available?",
"If cash flow is limiting their order size:",
"This is where I would connect to the \"buy deep\" strategy.",
"Neato used Slope to buy deeper, pay suppliers earlier, and improve margin after financing costs.",
"What does your cash conversion cycle look like from supplier payment to Amazon payout?",
"Are you usually paying suppliers before cash comes back from Amazon?",
"Has DD+7 or Amazon reserves changed your cash timing at all?",
"If cash is tied up in the cycle, I would position Slope as a way to separate supplier payment timing from Amazon payout timing.",
"When is your next real capital event?",
"Next supplier payment?", "Next inventory order?", "Next product launch or PPC push?", "Next debt payment?",
"If the timing is soon:",
"I would walk them through what a first draw would look like.",
"Compare the cost of the draw against the business outcome.",
"If the numbers make sense, offer to help complete the first draw while we are on the call.",
],
"o1": [
"I forgot about it / have not gotten around to it",
"Totally fair, that happens. The line is already approved, so I would just want to quickly walk you through what is available and see if there is a real use case coming up.",
"Main thing I would ask is: when is your next supplier payment, inventory order, debt payment, or PPC push?",
],
"o2": [
"I asked for $300K and only got $250K",
"I get that. I would frame the $250K as the starting point, not necessarily the ceiling.",
"As you draw, repay, and build history with Slope, that can help support future line increases. National Bobblehead went from $170K to $250K after additional documentation.",
],
"o3": [
"The rate seems high or confusing",
"Totally fair. I would want to walk through the actual dollar cost of a draw, because APR and total financing cost can be easy to mix up.",
"The real question is whether the capital creates more value than it costs, like supplier discounts, avoided stockouts, debt payoff, or buying deeper.",
],
"o4": [
"Amazon Lending is working fine for me",
"That is good to hear. I would not tell you to stop using something that works.",
"I would position Slope as an additional flexible line outside of Amazon's timing, offer size, disbursements, and repayment structure.",
],
"o5": [
"I have not heard of Slope",
"Totally understandable. A lot of sellers first hear about Slope through the Amazon or marketplace offer.",
"I would point to the J.P. Morgan credit facility, Lead Bank origination, and customer stories like National Bobblehead, Neato, and Continental Cards.",
],
"o6": [
"I am not sure what I would use it for right now",
"That is exactly what I would want to figure out before recommending a draw.",
"I would look at upcoming supplier payments, inventory orders, PPC, product launches, expensive debt, or supplier discounts to see if there is a real use case.",
],
"o7": [
"I am confused on how the draw and repayment process actually works",
"You draw through the Slope portal, choose the amount and repayment term, and funds go to your business bank account.",
"Repayment is not a daily revenue sweep from Amazon. You know the schedule upfront, and the line replenishes as you repay.",
],
"o8": [
"Let me think about it / not right now",
"Of course. I would just want to understand what part you want to think through: rate, timing, line size, trust, or use case.",
"If there is no real use case right now, that is fine. I would schedule the follow-up around the next supplier payment, restock, or growth event.",
],
"pos": [
"How would you position Slope?",
"Slope is an AI-native working capital platform built specifically for e-commerce sellers. We are backed by J.P. Morgan, both as an investor and credit facility partner, and we work directly with Amazon, Walmart, and Alibaba as a financing partner. The product is a reusable line of credit. You apply once, with no impact to your personal credit score and no personal guaranty required. Once approved, you can draw capital as needed, set a fixed repayment schedule at the time of each draw, and repay without the schedule accelerating based on revenue volume. As each draw is repaid, the line replenishes and becomes available for the next inventory cycle.",
"The value is not just access to capital. It is control over timing. Slope gives sellers working capital outside of the Amazon disbursement cycle, so they can separate their purchasing timeline from their payout timeline. That allows them to buy earlier, buy deeper, pay suppliers sooner, capture volume discounts, and prepare for peak demand before cash would otherwise be available. In many cases, that creates margin on the COGS side, where early payment, larger orders, and better supplier timing can reduce costs by 15 to 22 percent on a single purchase order. Neato, for example, increased margin by 5.5 percent after using Slope financing to buy deep and early. That is the core position: Slope is not just a lender. It is a capital partner that helps sellers move faster, protect margin, and keep inventory cycles running without being constrained by marketplace payout timing.",
],
"draw": [
"I would not push for a draw until I understand the use case. My goal would be to find the cleanest business reason to activate, then walk them through the first draw if the numbers make sense.",
"Approval / confusion",
"→ If they forgot about it, quickly re-orient them: $250K approved, first draw has 20% off interest, line is ready when the timing makes sense",
"→ If APR or fees are confusing, walk through the actual dollar cost of a sample draw",
"→ Once they understand the line, move into use case",
"Original $300K request",
"→ What was it for? Inventory, supplier payment, PPC, product launch, debt payoff, or seasonal demand?",
"→ Is that need still active?",
"→ When do they need the capital?",
"Amazon Lending",
"→ If Amazon Lending has pain around access, repayment, or use of funds, position Slope as the stronger alternative",
"→ If Amazon Lending is working well, position Slope as an additional line that can run in parallel",
"→ The goal is not to force a replacement, it is to give them more flexibility",
"If supplier payment or inventory order is coming up soon",
"→ Ask when the payment is due and how they planned to fund it",
"→ Compare Slope against Amazon Lending, cash on hand, or other financing",
"→ If the numbers make sense, walk them through the draw amount, term, repayment schedule, and cost on the call",
"If buying deeper creates margin",
"→ Ask if suppliers offer volume discounts or early-payment discounts",
"→ Connect to Neato: they used Slope to buy deeper, pay suppliers earlier, and improve margin after financing costs",
"→ Position the draw as margin capture, not just borrowing money",
"If cash is tied up between supplier payment and Amazon payout",
"→ Position Slope as a way to separate their purchasing timeline from Amazon’s payout timeline",
"→ If the next inventory order, PPC push, or launch is coming up soon, walk through the draw while on the call",
"Current financing",
"→ Are they carrying MCA, revenue-based financing, credit card debt, or another short-term loan?",
"→ If yes, compare the cost of that debt against Slope",
"→ Connect to National Bobblehead: they used their first Slope draw to pay off a higher-cost merchant cash advance",
"→ Position the draw as a way to lower financing cost if the payoff math works",
"If they do not need capital right now",
"→ Do not force the draw",
"→ Make sure they understand the line and schedule follow-up around the next supplier payment, inventory order, launch, or PPC push",
"→ Only suggest a small test draw if they expect to use the line soon and want to get comfortable with the portal before a larger payment is due",
"Close:",
"“Based on what you told me, it sounds like the clearest use case is [supplier payment / inventory order / debt payoff / buying deeper / PPC or launch]. Since I already have you on the phone, I’m happy to help you pull up the portal and walk you through the dashboard: what your available credit means, how to select a draw amount, how the repayment term works, and what the total cost would look like.",
"If the capital need is coming up soon:",
"Since that payment is coming up on [date], we can walk through your first real draw now. I can show you the amount, term, repayment schedule, and total cost before you confirm anything. If the numbers make sense, we can get it started while we are on the call.",
"If the capital need is further out:",
"Since you do not need the full capital right away, one option is a small test draw so you can get comfortable with the portal and repayment flow before a larger payment is due, especially with the 20% interest discount on the first draw. If you would rather wait, that is completely fine too. I can follow up a few days before [capital event] and walk you through it then.”",
],
}

# bubble line (outside popups)
bubble_expect = "How would you get a customer to complete a first draw?"

fails = 0
for pid, lines in EXPECTED.items():
    txt = popup_text(pid)
    pos = 0
    for ln in lines:
        n = norm(ln)
        idx = txt.find(n, pos)
        if idx < 0:
            fails += 1
            print(f"FAIL [{pid}]: missing or out of order:\n   {n[:110]}")
        else:
            pos = idx + len(n)
    else:
        pass
    print(f"OK   [{pid}] {len(lines)} lines verified" if all(norm(l) in txt for l in lines) else f"---- [{pid}] see failures above")

m = re.search(r'<div class="bubble-card">(.*?)</div>', doc, re.S)
btxt = norm(re.sub(r"<[^>]+>", " ", m.group(1))) if m else ""
if btxt == bubble_expect:
    print("OK   [bubble] verified")
else:
    fails += 1
    print(f"FAIL [bubble]: got '{btxt}'")

print("\nALL TEXT VERBATIM ✔" if fails == 0 else f"\n{fails} FAILURES ✘")
sys.exit(0 if fails == 0 else 1)
