import crypto from 'node:crypto';

const DIRECT_DISCOUNTS = Object.freeze({
  SPRING25: 25,
  WELCOME10: 10
});

export const DEFAULT_SIGNING_SECRET = 'wth-071-debug-secret';

const MAX_TOKEN_LENGTH = 512;

export const campaigns = Object.freeze({
  WMNSDY2026: {
    validFrom: Date.parse('2026-03-08T00:00:00.000Z'),
    validUntil: Date.parse('2026-03-08T23:59:59.999Z'),
    discount: 60
  },
  ORANGE2026: {
    validFrom: Date.parse('2026-05-04T00:00:00.000Z'),
    validUntil: Date.parse('2026-05-04T23:59:59.999Z'),
    discount: 40
  }
});

export function calculateDiscountFromCoupon(basketCoupon) {
  return DIRECT_DISCOUNTS[basketCoupon] ?? 0;
}

export function createSignedCouponToken(code, secret = DEFAULT_SIGNING_SECRET) {
  if (!(code in campaigns)) {
    throw new Error(`Unknown campaign code: ${code}`);
  }

  const payload = Buffer.from(JSON.stringify({ code }), 'utf8').toString('base64url');
  const signature = signPayload(payload, secret);

  return `${payload}.${signature}`;
}

export function calculateApplicableDiscount({
  basketCoupon,
  signedCouponData,
  now = Date.now(),
  secret = DEFAULT_SIGNING_SECRET
}) {
  const directDiscount = calculateDiscountFromCoupon(basketCoupon);
  if (directDiscount) {
    return directDiscount;
  }

  const campaign = parseSignedCampaign(signedCouponData, secret);
  if (!campaign) {
    return 0;
  }

  if (now < campaign.validFrom || now > campaign.validUntil) {
    return 0;
  }

  return campaign.discount;
}

function parseSignedCampaign(token, secret) {
  if (!token || token.length > MAX_TOKEN_LENGTH) {
    return null;
  }

  const parts = token.split('.');
  if (parts.length !== 2) {
    return null;
  }

  const [payload, signature] = parts;
  const expectedSignature = signPayload(payload, secret);
  if (!hasValidSignature(signature, expectedSignature)) {
    return null;
  }

  let parsedPayload;
  try {
    parsedPayload = JSON.parse(Buffer.from(payload, 'base64url').toString('utf8'));
  } catch {
    return null;
  }

  if (!parsedPayload || typeof parsedPayload.code !== 'string') {
    return null;
  }

  return campaigns[parsedPayload.code] ?? null;
}

function signPayload(payload, secret) {
  return crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('base64url');
}

function hasValidSignature(actual, expected) {
  const actualBuffer = Buffer.from(actual);
  const expectedBuffer = Buffer.from(expected);

  if (actualBuffer.length !== expectedBuffer.length) {
    return false;
  }

  return crypto.timingSafeEqual(actualBuffer, expectedBuffer);
}
