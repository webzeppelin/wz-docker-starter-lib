import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription} from "rxjs";
import { Router, ActivatedRoute} from '@angular/router';

import { UserInfo } from './shared/api.model'
import { ApiService } from './shared/api.service'
import { OIDCService } from './shared/oidc.service'

import '../style/app.scss';
import '../style/forms.scss';

@Component({
  selector: 'my-app', // <my-app></my-app>
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit, OnDestroy {
    private oidc_sub: Subscription;
    private ui_sub: Subscription;
    url = 'https://github.com/';
    userInfo: UserInfo;

    constructor(private api: ApiService, private oidc: OIDCService, private activatedRoute: ActivatedRoute) {
        this.userInfo = null;
    }

    handleLoginClick(): void {
        this.oidc.login();
    }

    handleLogoutClick(): void {
        this.oidc.logout();
    }

    isLoggedIn(): boolean {
        return this.oidc.isLoggedIn();
    }

    ngOnInit() {
        this.oidc_sub = this.activatedRoute.queryParams.subscribe(params => {
            let code = params["code"];
            if (code != null) {
                console.log("Handling IDP callback");
                let state = params["state"]
                if (state == null) {
                    throw new Error("Missing state in idp callback");
                }
                this.oidc.claimTokens(code, state);
            }
        });
        this.ui_sub = this.oidc.getUserInfo().subscribe(
            ui => this.handleUserInfoChange(ui),
            error => { throw new Error("Could not subscribe to user info changes") }
        );
        this.oidc.refreshUserInfo();
    }

    handleUserInfoChange(ui: UserInfo): void {
        this.userInfo = ui;
    }

    ngOnDestroy() {
        this.oidc_sub.unsubscribe();
        this.ui_sub.unsubscribe();
    }
}
