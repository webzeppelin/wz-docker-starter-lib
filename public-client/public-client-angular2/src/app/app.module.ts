import { NgModule, ApplicationRef } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { AlertModule, CarouselModule } from 'ng2-bootstrap/ng2-bootstrap';

import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';
import { ApiService } from './shared/api.service';
import { Configuration } from './app.config';

import { ClockComponent } from './shared/clock/clock.component';
import { SignGuestbookComponent } from './home/sign-guestbook/sign-guestbook.component';
import { BrowseGuestbookComponent } from './home/browse-guestbook/browse-guestbook.component';
import { SearchGuestbookComponent } from './home/search-guestbook/search-guestbook.component';

import { routing } from './app.routing';

import { removeNgStyles, createNewHosts } from '@angularclass/hmr';

@NgModule({
  imports: [
    BrowserModule,
    HttpModule,
    FormsModule,
    routing,
    AlertModule,
    CarouselModule
  ],
  declarations: [
    AppComponent,
    HomeComponent,
    AboutComponent,
    ClockComponent,
    SignGuestbookComponent,
    BrowseGuestbookComponent,
    SearchGuestbookComponent
  ],
  providers: [
    ApiService,
    Configuration
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(public appRef: ApplicationRef) {}
  hmrOnInit(store) {
    console.log('HMR store', store);
  }
  hmrOnDestroy(store) {
    let cmpLocation = this.appRef.components.map(cmp => cmp.location.nativeElement);
    // recreate elements
    store.disposeOldHosts = createNewHosts(cmpLocation);
    // remove styles
    removeNgStyles();
  }
  hmrAfterDestroy(store) {
    // display new elements
    store.disposeOldHosts();
    delete store.disposeOldHosts;
  }
}
