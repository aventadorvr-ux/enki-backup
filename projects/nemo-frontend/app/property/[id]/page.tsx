"use client";

import { PageTransition } from "@/components/animations";
import { MapPin, Bed, Bath, Maximize, Car, Share2, Heart, Phone, Mail, Check } from "lucide-react";

const propertyFeatures = ["Air Conditioning", "Heating", "Garage", "Garden", "Pool", "Smart Home"];

export default function PropertyDetailPage() {
  return (
    <PageTransition>
      <div className="min-h-screen bg-gray-50 pb-12 dark:bg-slate-900">
        <div className="relative h-[60vh] w-full">
          <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1600" alt="Property" className="h-full w-full object-cover" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
          <div className="absolute right-4 top-4 flex gap-2">
            <button className="flex h-10 w-10 items-center justify-center rounded-full bg-white/90 shadow-lg"><Share2 className="h-5 w-5" /></button>
            <button className="flex h-10 w-10 items-center justify-center rounded-full bg-white/90 shadow-lg"><Heart className="h-5 w-5" /></button>
          </div>
          <div className="absolute bottom-4 left-4">
            <span className="rounded-xl bg-white px-4 py-2 text-2xl font-bold text-gray-900 shadow-lg">$2,450,000</span>
          </div>
        </div>

        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-3">
            <div className="lg:col-span-2 space-y-8">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Modern Villa with Ocean Views</h1>
                <div className="mt-2 flex items-center gap-2 text-gray-500 dark:text-gray-400"><MapPin className="h-5 w-5" /><span>123 Beach Road, Auckland</span></div>
              </div>

              <div className="grid grid-cols-2 gap-4 rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-800 md:grid-cols-4">
                <div className="text-center"><Bed className="mx-auto h-6 w-6 text-primary-500" /><p className="mt-2 text-2xl font-bold dark:text-white">4</p><p className="text-sm text-gray-500">Bedrooms</p></div>
                <div className="text-center"><Bath className="mx-auto h-6 w-6 text-primary-500" /><p className="mt-2 text-2xl font-bold dark:text-white">3</p><p className="text-sm text-gray-500">Bathrooms</p></div>
                <div className="text-center"><Maximize className="mx-auto h-6 w-6 text-primary-500" /><p className="mt-2 text-2xl font-bold dark:text-white">320</p><p className="text-sm text-gray-500">m</p></div>
                <div className="text-center"><Car className="mx-auto h-6 w-6 text-primary-500" /><p className="mt-2 text-2xl font-bold dark:text-white">2</p><p className="text-sm text-gray-500">Garage</p></div>
              </div>

              <div className="rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-800">
                <h2 className="text-xl font-semibold dark:text-white">Description</h2>
                <p className="mt-4 text-gray-600 dark:text-gray-300">Experience luxury living at its finest in this stunning modern villa with breathtaking ocean views.</p>
              </div>

              <div className="rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-800">
                <h2 className="text-xl font-semibold dark:text-white">Features</h2>
                <div className="mt-4 grid grid-cols-2 gap-3">
                  {propertyFeatures.map((f) => (<div key={f} className="flex items-center gap-2"><Check className="h-5 w-5 text-secondary-500" /><span className="text-sm text-gray-600 dark:text-gray-300">{f}</span></div>))}
                </div>
              </div>
            </div>

            <div className="space-y-6">
              <div className="rounded-2xl bg-white p-6 shadow-sm dark:bg-slate-800">
                <h3 className="text-lg font-semibold dark:text-white">Contact Agent</h3>
                <div className="mt-4 flex items-center gap-4">
                  <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary-100 text-xl font-bold text-primary-600">S</div>
                  <div><p className="font-semibold dark:text-white">Sarah Mitchell</p><p className="text-sm text-gray-500">Premium Agent</p></div>
                </div>
                <div className="mt-4 space-y-2">
                  <button className="flex w-full items-center justify-center gap-2 rounded-xl bg-primary-500 py-3 font-medium text-white hover:bg-primary-600"><Phone className="h-4 w-4" />Call Agent</button>
                  <button className="flex w-full items-center justify-center gap-2 rounded-xl border border-gray-200 bg-white py-3 font-medium text-gray-700 hover:bg-gray-50"><Mail className="h-4 w-4" />Send Email</button>
                </div>
              </div>

              <div className="rounded-2xl bg-gradient-to-br from-primary-500 to-primary-600 p-6 text-white">
                <h3 className="text-lg font-semibold">AI Valuation</h3>
                <p className="mt-3 text-3xl font-bold">$2,380,000 - $2,520,000</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
