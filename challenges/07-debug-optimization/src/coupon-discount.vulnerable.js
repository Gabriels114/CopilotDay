const DIRECT_DISCOUNTS = Object.freeze({
  SPRING25: 25,
  WELCOME10: 10
});

export const campaigns = Object.freeze({
  WMNSDY2026: {
    validOn: Date.parse('2026-03-08T00:00:00.000Z'),
    discount: 60
  },
  ORANGE2026: {
    validOn: Date.parse('2026-05-04T00:00:00.000Z'),
    discount: 40
  }
});

export function calculateDiscountFromCoupon(basketCoupon) {
  return DIRECT_DISCOUNTS[basketCoupon] ?? 0;
}

export function calculateApplicableDiscount({ basketCoupon, couponData }) {
  const directDiscount = calculateDiscountFromCoupon(basketCoupon);
  if (directDiscount) {
    return directDiscount;
  }

  if (!couponData) {
    return 0;
  }

  const [couponCode, couponDate] = Buffer.from(couponData, 'base64')
    .toString('utf8')
    .split('-');

  const campaign = campaigns[couponCode];

  if (campaign && couponDate == campaign.validOn) {
    return campaign.discount;
  }

  return 0;
}
