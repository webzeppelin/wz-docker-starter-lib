import { Component } from '@angular/core';

import { ApiService } from './shared/api.service';

import '../style/app.scss';
import '../style/forms.scss';

@Component({
  selector: 'my-app', // <my-app></my-app>
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  url = 'https://github.com/';

  constructor(private api: ApiService) {
    // Do something with api
  }
}
