import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import { Router } from '@angular/router';
import { ApiService } from './api.service'
import { LoginResponse, TokenResponse, TokenRequest, UserInfo } from './api.model'
import { Cookie } from 'ng2-cookies/ng2-cookies';

import 'rxjs/Rx'
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import 'rxjs/add/operator/map'

import { Configuration } from '../app.config';

@Injectable()
export class OIDCService {
    private _user: BehaviorSubject<UserInfo>;

    constructor(private _api: ApiService, private _configuration: Configuration, private _router: Router) {
        this._user = new BehaviorSubject<UserInfo>(new UserInfo('Loading...','',''));
    }

    public isLoggedIn (): boolean {
        if (Cookie.get('wzstarter.oidc.id_token')) {
            return true;
        } else {
            return false;
        }
    }

    public getAccessToken (): string {
        return Cookie.get('wzstarter.oidc.access_token');
    }

    public getIdentityToken (): string {
        return Cookie.get('wzstarter.oidc.id_token');
    }

    public login (): void {
        this._api.startLogin()
            .subscribe(
                lr => this.handle_start_login_response(lr),
                error => console.error('Error: ' + error)
            );
    }

    private handle_start_login_response ( loginResponse: LoginResponse ): void {
        console.log('Got start login response' + loginResponse);
        Cookie.set('wzstarter.login.session_id',loginResponse.session_id);

        // redirect to idp for authentication
        console.log("initial state: "+loginResponse.state);
        window.location.href = loginResponse.login_url;
    }

    public claimTokens ( code: string, state: string): void {
        let session_id = Cookie.get('wzstarter.login.session_id');
        console.log("claim code: "+code);
        console.log("final state: "+state);
        if (!session_id)
        {
            throw new Error("Missing login session_id cookie");
        }

        let request = new TokenRequest(session_id, state, code);
        this._api.claimTokens(request)
            .subscribe(
                tr => this.handle_claim_tokens_response(tr),
                error => console.error('Error: ' + error)
            );
    }

    private handle_claim_tokens_response ( tokenResponse: TokenResponse ): void {
        console.log('Got get token response' + tokenResponse);
        Cookie.set('wzstarter.oidc.id_token', tokenResponse.id_token);
        Cookie.set('wzstarter.oidc.access_token', tokenResponse.access_token);
        Cookie.set('wzstarter.oidc.expires_in', tokenResponse.expires_in);
        Cookie.delete('wzstarter.login.session_id');

        // redirect to the home page
        this.refreshUserInfo();
        this._router.navigate(["/"]); /*.then(result=>{window.location.href = '/';});*/
    }

    public getUserInfo (): Observable<UserInfo> {
        return this._user.asObservable();
    }

    public refreshUserInfo (): void {
        if (!this.isLoggedIn()) return;

        this._api.getUserInfo()
            .subscribe(
                ui => this.handleRefreshUserInfoResponse(ui),
                error => console.error('Error: ' + error)
            );
    }

    private handleRefreshUserInfoResponse ( userInfo: UserInfo ): void {
        this._user.next(userInfo);
    }

    public logout(): void {
        Cookie.delete('wzstarter.oidc.id_token');
        Cookie.delete('wzstarter.oidc.access_token');
        Cookie.delete('wzstarter.oidc.expires_in');
    }
}