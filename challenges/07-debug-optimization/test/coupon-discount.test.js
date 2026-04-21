import assert from 'node:assert/strict';
import test from 'node:test';

import {
  calculateApplicableDiscount as calculateFixedDiscount,
  campaigns as fixedCampaigns,
  createSignedCouponToken,
  DEFAULT_SIGNING_SECRET
} from '../src/coupon-discount.fixed.js';
import {
  calculateApplicableDiscount as calculateVulnerableDiscount,
  campaigns as vulnerableCampaigns
} from '../src/coupon-discount.vulnerable.js';

test('la version vulnerable acepta un cupon forjado en base64', () => {
  const forgedCoupon = Buffer.from(
    `WMNSDY2026-${vulnerableCampaigns.WMNSDY2026.validOn}`,
    'utf8'
  ).toString('base64');

  assert.equal(
    calculateVulnerableDiscount({ couponData: forgedCoupon }),
    vulnerableCampaigns.WMNSDY2026.discount
  );
});

test('la version corregida rechaza el payload base64 sin firma', () => {
  const forgedCoupon = Buffer.from(
    `WMNSDY2026-${vulnerableCampaigns.WMNSDY2026.validOn}`,
    'utf8'
  ).toString('base64');

  assert.equal(
    calculateFixedDiscount({
      signedCouponData: forgedCoupon,
      now: fixedCampaigns.WMNSDY2026.validFrom,
      secret: DEFAULT_SIGNING_SECRET
    }),
    0
  );
});

test('la version corregida acepta un token firmado dentro de la ventana valida', () => {
  const signedCoupon = createSignedCouponToken('WMNSDY2026', DEFAULT_SIGNING_SECRET);

  assert.equal(
    calculateFixedDiscount({
      signedCouponData: signedCoupon,
      now: Date.parse('2026-03-08T12:00:00.000Z'),
      secret: DEFAULT_SIGNING_SECRET
    }),
    fixedCampaigns.WMNSDY2026.discount
  );
});

test('la version corregida rechaza un token manipulado', () => {
  const signedCoupon = createSignedCouponToken('WMNSDY2026', DEFAULT_SIGNING_SECRET);
  const [payload, signature] = signedCoupon.split('.');
  const tamperedPayload = Buffer.from(JSON.stringify({ code: 'ORANGE2026' }), 'utf8')
    .toString('base64url');
  const tamperedToken = `${tamperedPayload}.${signature}`;

  assert.equal(
    calculateFixedDiscount({
      signedCouponData: tamperedToken,
      now: Date.parse('2026-05-04T12:00:00.000Z'),
      secret: DEFAULT_SIGNING_SECRET
    }),
    0
  );
});

test('la version corregida mantiene descuentos directos sin depender del token', () => {
  const expiredCoupon = createSignedCouponToken('WMNSDY2026', DEFAULT_SIGNING_SECRET);

  assert.equal(
    calculateFixedDiscount({
      basketCoupon: 'WELCOME10',
      signedCouponData: expiredCoupon,
      now: Date.parse('2026-04-01T12:00:00.000Z'),
      secret: DEFAULT_SIGNING_SECRET
    }),
    10
  );
});
